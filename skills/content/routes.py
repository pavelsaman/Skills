from flask import redirect, url_for, render_template, request
from skills.content.forms import SkillForm, CategoryForm
from flask_login import login_required, current_user
from skills.models import Category, Skill
from config import ErrorMessages, Config
from skills.content import bp


@bp.before_request
def generate_new_token():
    if current_user.is_authenticated:
        if current_user.token_is_expired():
            current_user.set_new_token()


@bp.route('/auth', methods=['GET', 'POST'])  # this route accepts POST method as well, default is just GET
@bp.route('/auth/', methods=['GET', 'POST'])
@bp.route('/auth/index', methods=['GET', 'POST'])
@login_required
def index():
    form = SkillForm(request.form)
    form.update_category_choices()
    # adding a new skill
    if request.method == 'POST' and 'skill' in request.form.keys() and 'new_category' not in request.form.keys():
        if form.validate() and form.no_special_characters():
            if Skill.insert_new_skill(form.skill.data, dict(form.category.choices).get(form.category.data)):
                return redirect(url_for('main.index'))
            else:
                form.add_error(ErrorMessages.SKILL_NOT_UNIQUE)
    # going to category form
    elif request.method == 'POST' and 'skill' in request.form.keys() and 'new_category' in request.form.keys():
        return redirect(url_for('content.category'))
    return render_template('content/index.html', result_set=Skill.get_all_visible_skills(), form=form,
                           admin_email=Config.ADMIN_EMAIL)


# adding a new category
@bp.route('/category/', methods=['GET', 'POST'])
@bp.route('/category', methods=['GET', 'POST'])
@bp.route('/auth/category/', methods=['GET', 'POST'])
@bp.route('/auth/category', methods=['GET', 'POST'])
@login_required
def category():
    form = CategoryForm(request.form)
    # adding a new category
    if request.method == 'POST' and 'go_back' not in request.form.keys():
        if form.validate() and form.no_special_characters():
            if Category.insert_new_category(form.category.data):
                return redirect(url_for('main.index'))
            else:
                form.add_error(ErrorMessages.CATEGORY_NOT_UNIQUE)
    elif request.method == 'POST' and 'go_back' in request.form.keys():  # going back to main page
        return redirect(url_for('main.index'))
    return render_template('content/index.html', result_set=Skill.get_all_visible_skills(), form=form,
                           admin_email=Config.ADMIN_EMAIL)


# skill deletion
@bp.route('/auth/delete/', methods=['GET', 'POST'])
@bp.route('/auth/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'POST':
        Skill.delete_skill(list(request.form.keys())[0])
    return redirect(url_for('content.index'))
