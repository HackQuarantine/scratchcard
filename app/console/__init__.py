from flask import Blueprint

console = Blueprint(
    'console',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from . import views
