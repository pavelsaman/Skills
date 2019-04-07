from flask import Blueprint

bp = Blueprint('errors', __name__)

from skills.errors import handlers
