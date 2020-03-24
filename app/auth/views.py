from . import hqauth, process_userinfo
from flask_login import login_user, login_required, logout_user
from flask import redirect, url_for, flash
from app.db import db, User

from app import config

# this fetches the user info from the oauth server and then
# loads them into our database.
@hqauth.route('/connect')
def connect():
    try:
        user_info = hqauth.session.get(config.USER_INFO).json()
    except:
        flash('Unable to login, try again', 'warning')
        return redirect(url_for('home.homepage'))


    # handle the weird cases that may cause issues.
    if not user_info:
        flash('unable to login, try again', 'warning')
        return redirect(url_for('home.homepage'))

    # Only allow users with verified emails to use the service.
    if user_info['email_verified'] is False:
        flash('Please verify your email! Then click login!')
        return redirect(url_for('home.homepage'))

    # Login / create the user
    curr = User.query.get(user_info['sub'])
    if curr is None:
        curr = process_userinfo(user_info)
        db.session.add(curr)
        db.session.commit()

    login_user(curr)
    flash('You are now logged in!', 'success')
    return redirect(url_for('console.consolepage'))

@hqauth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.homepage'))
