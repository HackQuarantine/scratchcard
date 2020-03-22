from . import hqauth
from flask_login import login_user, login_required, logout_user
from flask import redirect, url_for, flash
from app.db import db, User

from app import config

# this fetches the user info from the oauth server and then
# loads them into our database.
@hqauth.route('/connect')
def connect():
    user_info = hqauth.session.get(config.USER_INFO).json()
    print(user_info)
    if not user_info:
        flash('unable to login, try again', 'warning')
        return redirect('home.homepage')
    curr = User.query.get(user_info['sub'])
    if curr is None:
        curr = User()
        curr.id = user_info['sub']
        curr.username = user_info['name']
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
