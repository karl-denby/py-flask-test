#
# Imports
#
from sys import version
from flask import Flask, redirect, request, render_template, session, flash, g
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import sqlite3


#
# Classes
#
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MySecretKeyForCSFR'
bootstrap = Bootstrap(app)
moment = Moment(app)


#
# sqlite3 boilerplate from http://flask.pocoo.org/docs/0.11/patterns/sqlite3/
#
DATABASE = '/path/to/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#
# routes/controllers
#
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
        old_name = session.get('name')
        if old_name != test_form.name.data:
            flash("You've changed your name")
            session['name'] = test_form.name.data

    if session.get('name') == None:
        who = 'Anonymous'
    else:
        who = session['name']
    return render_template('user.html', name=who, form=test_form)


#
# Run the application
#
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
