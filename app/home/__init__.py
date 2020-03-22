from flask import Blueprint

home = Blueprint(
    'home',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from . import views
