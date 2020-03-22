from flask import Flask, session
from flask_caching import Cache
from flask_bootstrap import Bootstrap

from app.auth import hqauth as auth, login_manager
from app.home import home
from app.admin import admin
from app.console import console
from app import config, db as database



def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
    app.config['CACHE_TYPE'] = 'simple'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    app.config['NAME'] = config.NAME or 'cd'

    cache = Cache(app)
    bootstrap = Bootstrap(app)

    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(console, url_prefix='/console')
    app.register_blueprint(auth, url_prefix='/login')
    app.register_blueprint(home, url_prefix='/')

    database.db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        database.db.create_all()
    return app

if __name__ == '__main__':
    create_app()
