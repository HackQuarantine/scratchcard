from flask import Flask, request, redirect, flash, url_for
from flask_dance.consumer import OAuth2ConsumerBlueprint
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_login import LoginManager
from app import config
from app.db import db, OAuth, User


login_manager = LoginManager()
login_manager.session_protection = "strong"

# Extract everything to be loaded into our local DB
def process_userinfo(user_info):
    curr = User()
    curr.id = user_info['sub']
    curr.username = user_info['name']
    if 'https://hackquarantine.com/user_metadata' in user_info:
        curr.student_status = bool(user_info['https://hackquarantine.com/user_metadata']['student_status']) or False
    # only me, hacky but quick
    curr.admin = (user_info['sub'] == config.ADMIN_ID)
    return curr

@login_manager.user_loader
def userloader(user_id):
    curr = User.query.get(user_id)
    if curr is None:
        user_info = hqauth.session.get(config.USER_INFO).json()
        curr = process_userinfo(user_info)
        db.session.add(curr)
        db.session.commit()
    return curr


@login_manager.unauthorized_handler
def unauthorized():
    flash('Please login', 'warning')
    return redirect(url_for('home.homepage'))

hqauth = OAuth2ConsumerBlueprint(
    'oauth',
    __name__,
    base_url=config.BASE_URL,
    token_url=config.ACCESS_TOKEN_URL,
    authorization_url=config.AUTHORIZE_URL,
    client_id=config.CLIENT_ID,
    client_secret=config.CLIENT_SECRET,
    scope=config.OAUTH_SCOPE,
    redirect_to='oauth.connect'
)


from . import views
