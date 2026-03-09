from flask import Blueprint

alumnos = Blueprint('alumnos', __name__)

from . import routes