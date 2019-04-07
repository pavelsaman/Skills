from flask import Blueprint

bp = Blueprint('content', __name__)

from skills.content import forms, routes
