from flask import render_template, redirect, url_for
from flask_login import current_user
from skills.models import Skill
from skills.main import bp
from config import Config
from skills import db


@bp.route('/index/', methods=['GET'])
@bp.route('/index', methods=['GET'])
@bp.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('content.index'))
    return render_template('index.html', result_set=Skill.get_all_visible_skills(), admin_email=Config.ADMIN_EMAIL)


@bp.teardown_request
def remove_db_session(exception):
    db.session.remove()
