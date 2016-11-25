from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, request
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm


@main.route('/')
def hello_world():
    return render_template('index.html', current_time=datetime.utcnow())

@main.route('/headers')
def headers():
    user_agent = request.headers.get('User-Agent')
    return render_template('headers.html', user_agent=user_agent)


@main.route('/user/', methods=['GET', 'POST'])
@main.route('/user/<name>', methods=['GET', 'POST'])
def user(name=None):
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            #send_email(current_app.config['MAIL_ADMIN'], 'New User', 'mail/new_user', user=user)
            session['known'] = False
        else:
            session['known'] = True

        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.user'))

    return render_template(
        'user.html',
        form=form,
        name=session.get('name'),
        known=session.get('known', False)
    )
