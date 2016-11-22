#
# Imports
#
from sys import version
import os
from datetime import datetime
import sqlite3

from flask import Flask, redirect, request, render_template, session, flash, g
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'MySecretKeyForCSFR'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


#
# Classes
#
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


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
