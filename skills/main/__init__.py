from flask import Blueprint

bp = Blueprint('main', __name__)

from skills.main import routes
