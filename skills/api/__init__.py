from flask import Blueprint

bp = Blueprint('api', __name__)

from skills.api import skills, errors, validations
