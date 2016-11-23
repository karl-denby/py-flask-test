#
# Imports
#
from sys import version
import os
from datetime import datetime
import sqlite3

from flask import Flask, redirect, request, render_template, session, flash, g, url_for
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
manager = Manager(app)

bootstrap = Bootstrap(app)
moment = Moment(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

app.config['SECRET_KEY'] = 'MySecretKeyForCSFR'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))


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
    user = db.relationship('User', backref='role', lazy='dynamic')

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
    form = NameForm()
    if form.validate_on_submit():
        db_user = User.query.filter_by(username=form.name.data).first()
        if db_user is None:
            db_user = User(username=form.name.data)
            db.session.add(db_user)
            session['known'] = False
        else:
            session['known'] = True

        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('user'))

    return render_template(
        'user.html',
        form=form,
        name=session.get('name'),
        known=session.get('known', False)
    )


#
# Run the application
#
if __name__ == '__main__':
    manager.run()
    #app.run(debug=True, host='0.0.0.0')
