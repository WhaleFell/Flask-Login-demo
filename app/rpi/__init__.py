from flask import Blueprint

rpi = Blueprint('rpi', __name__)

from . import views
