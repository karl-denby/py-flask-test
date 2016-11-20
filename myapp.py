from sys import version
from flask import Flask, redirect, request, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MySecretKeyForCSFR'
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def hello_world():
    return render_template('index.html', current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/headers')
def headers():
    user_agent = request.headers.get('User-Agent')
    return render_template('headers.html', user_agent=user_agent)

@app.route('/user/', methods=['GET', 'POST'])
@app.route('/user/<name>', methods=['GET', 'POST'])
def user(name=None):
    test_form = NameForm()
    if test_form.validate_on_submit():
        name = test_form.name.data
        test_form.name.data = ''
        
    if name == None:
        name = "Anonymous"
        
    return render_template('user.html', name=name, form=test_form)


#
# Run the application
#
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
