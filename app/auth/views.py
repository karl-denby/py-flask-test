from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user
from . import auth
from .. import models
from .forms import LoginForm

@auth.route('/login', method=['GET', 'POST'])
def login():
    form = LoginForm()
    user = User.query.filter_by(email=form.email.data).first()

    if user is not None and user.verify_password(form.password.data):
        login_user(user, form.remember_me.data)
        return redirect(request.args.get('next')) or url_for('main.index')

    flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)
