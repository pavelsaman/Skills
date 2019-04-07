from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from config import Config, ErrorMessages
from skills.models import Category
from flask_wtf import FlaskForm


class SkillForm(FlaskForm):
    skill = StringField('skill', validators=[DataRequired(message=ErrorMessages.SKILL_REQUIRED),
                                             Length(min=Config.MIN_SKILL_LENGTH, max=Config.MAX_SKILL_LENGTH,
                                                    message=ErrorMessages.SKILL_TOO_MANY_CHARS)])
    category = SelectField('category', choices=[(str(c.id_skill_cat), c.category_name) for c in
                                                Category.query.filter_by(is_shown=True)])
    add = SubmitField('add')
    new_category = SubmitField('new_category')

    # if I name this validate, then validators like DataRequired() won't apply
    def no_special_characters(self):
        for c in self.skill.data:
            if c in Config.FORBIDDEN_CHARACTERS:
                self.add_error(ErrorMessages.SKILL_INVALID_CHARACTERS)
                return False
        return True

    def add_error(self, message):
        errors = list(self.skill.errors)
        errors.append(message)
        self.skill.errors = errors

    def update_category_choices(self):
        self.category.choices = [(str(c.id_skill_cat), c.category_name) for c in
                                 Category.query.filter_by(is_shown=Config.VISIBLE_ON_FE)]


class CategoryForm(FlaskForm):
    category = StringField('category', validators=[DataRequired(message=ErrorMessages.CATEGORY_REQUIRED),
                                                   Length(min=Config.MIN_CATEGORY_LENGTH,
                                                          max=Config.MAX_CATEGORY_LENGTH,
                                                          message=ErrorMessages.CATEGORY_TOO_MANY_CHARS)])
    new_category = SubmitField('new_category')
    go_back = SubmitField('go_back')

    # if I name this validate, then validators like DataRequired() won't apply
    def no_special_characters(self):
        for c in self.category.data:
            if c in Config.FORBIDDEN_CHARACTERS:
                self.add_error(ErrorMessages.CATEGORY_INVALID_CHARACTERS)
                return False
        return True

    def add_error(self, message):
        errors = list(self.category.errors)
        errors.append(message)
        self.category.errors = errors
