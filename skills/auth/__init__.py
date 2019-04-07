from flask import Blueprint

bp = Blueprint('auth', __name__)

from skills.auth import oauth, emails, routes
