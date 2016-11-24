from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, sender='noreply@myserver.com', recipients=to)
    msg.body = render_template( template + '.txt', **kwargs)
    msg.html = render_template( template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

#
# Views
#
@app.route('/')
def hello_world():
    return render_template('index.html', current_time=datetime.utcnow())

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
            send_email(app.config['MAIL_ADMIN'], 'New User', 'mail/new_user', user=db_user)
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
