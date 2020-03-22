from flask import render_template
from flask_login import current_user
from . import home

@home.route('/')
def homepage():
    return render_template('content.html')

