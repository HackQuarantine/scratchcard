from flask import Flask, request, redirect, flash, url_for
from flask_dance.consumer import OAuth2ConsumerBlueprint
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_login import LoginManager
from app import config
from app.db import db, OAuth, User


login_manager = LoginManager()
login_manager.session_protection = "strong"

@login_manager.user_loader
def userloader(user_id):
    curr = User.query.get(user_id)
    if curr is None:
        print('FETCHING')
        user_info = hqauth.session.get(config.USER_INFO).json()
        curr = User()
        curr.id = user_info['sub']
        curr.username = user_info['name']
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
