from flask_login import UserMixin
from datetime import timedelta
from datetime import datetime
from config import Config
from skills import db, lm
from flask import url_for
import string
import random
import copy


def init_db():
    db.create_all()


def to_collection_dict(obj):
    resources = obj.query.all()
    data = {
        'items': [item.to_dict('name') for item in resources],
        '_links': {
            'self': url_for('api.get_skills') if obj.__dict__['__tablename__'] == 'skill' else
            url_for('api.get_categories')
        }
    }
    return data


class Timestamp:
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)


class Category(Timestamp, db.Model):  # 1 side of the relationship
    __tablename__ = 'category'  # the name of my actual table
    id_skill_cat = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(Config.MAX_CATEGORY_LENGTH), unique=True, nullable=False)
    is_shown = db.Column(db.Boolean, default=True)
    skills = db.relationship('Skill', backref='category', lazy='dynamic')

    def __init__(self, name, is_shown=True):
        self.category_name = name
        self.is_shown = is_shown
        self.test = 4

    def __repr__(self):
        return "<Category: {self.id_skill_cat}, {self.category_name}, {self.is_shown}" \
               ", {self.updated}, {self.created}>".format(self=self)

    def __str__(self):
        return self.category_name

    def to_dict(self, call):
        data = {
            'category_id': self.id_skill_cat,
            'category_name': self.category_name,
            'is_shown': self.is_shown,
            'skills': [s.skill_name for s in self.get_all_skills()],
            'created': self.created.isoformat() + 'Z',  # time is in UTC, format ISO 8601
            '_links': {
                'self': url_for('api.get_category_by_name', category_name=self.category_name) if call == 'name' else
                url_for('api.get_category_by_id', category_id=self.id_skill_cat),
                'next': Config.NULL_API_RESPONSE,
                'previous': Config.NULL_API_RESPONSE
            }
        }
        all_categories = db.session.query(Category).order_by(Category.id_skill_cat).all()
        self_index = -1
        for i in range(len(all_categories)):
            if all_categories[i].category_name == self.category_name:
                self_index = i
                break
        if self_index < len(all_categories) - 1 and self_index != -1:
            next_cat = Category.query.filter_by(id_skill_cat=all_categories[self_index + 1].id_skill_cat).first()
            data['_links']['next'] = \
                data['_links']['next'] = \
                url_for('api.get_category_by_name', category_name=next_cat.category_name) if call == 'name' \
                else url_for('api.get_category_by_id', category_id=next_cat.id_skill_cat)
        if self_index > 0 and self_index != -1:
            previous_cat = Category.query.filter_by(id_skill_cat=all_categories[self_index - 1].id_skill_cat).first()
            data['_links']['previous'] = \
                url_for('api.get_category_by_name', category_name=previous_cat.category_name) if call == 'name' \
                else url_for('api.get_category_by_id', category_id=previous_cat.id_skill_cat)
        return data

    def get_all_skills(self):
        return self.skills

    @staticmethod
    def insert_new_category(category_name, is_shown=True):
        show = False
        if is_shown or is_shown == 1:
            show = True
        if Category.query.filter_by(category_name=category_name).first() is None \
                and len(category_name) <= Config.MAX_CATEGORY_LENGTH:
            new_category = Category(category_name, show)
            db.session.add(new_category)
            db.session.commit()
            return True
        return False

    @staticmethod
    def delete_category(category_name):
        category_to_be_deleted = Category.query.filter_by(category_name=category_name).first()
        if category_to_be_deleted is not None:
            if len(Skill.query.filter_by(id_cat=category_to_be_deleted.id_skill_cat).all()) == Config.EMPTY:
                db.session.delete(category_to_be_deleted)
                db.session.commit()
                return True
        return False


class Skill(Timestamp, db.Model):  # N side of the relationship
    __tablename__ = 'skill'  # the name of my actual table
    id_skill = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(Config.MAX_SKILL_LENGTH), unique=True, nullable=False)
    is_shown = db.Column(db.Boolean, default=True)
    id_cat = db.Column(db.Integer, db.ForeignKey(Category.id_skill_cat))

    def __init__(self, name, cat_name=None, is_shown=True):
        self.skill_name = name
        self.is_shown = is_shown
        if cat_name is not None:  # if a category has been received
            cat = Category.query.filter_by(category_name=cat_name).first()
            if cat is not None:  # if the category already exists
                self.id_cat = cat.id_skill_cat
            else:  # if the category doesn't exist, create a new one
                new_cat = Category(cat_name)
                db.session.add(new_cat)
                db.session.commit()
                self.id_cat = new_cat.id_skill_cat

    def __repr__(self):
        return "<Skill: {self.skill_name}, {self.category}, {self.created}, {self.updated}, " \
               ", {self.updated}, {self.created}>".format(self=self)

    def __str__(self):
        return self.skill_name

    def to_dict(self, call):
        data = {
            'skill_id': self.id_skill,
            'skill_name': self.skill_name,
            'is_shown': self.is_shown,
            'category_name': Category.query.filter_by(id_skill_cat=self.id_cat).first().category_name,
            'created': self.created.isoformat() + 'Z',  # time is in UTC, format ISO 8601
            '_links': {
                'self': url_for('api.get_skill_by_name', skill_name=self.skill_name) if call == 'name' else
                url_for('api.get_skill_by_id', skill_id=self.id_skill),
                'next': Config.NULL_API_RESPONSE,
                'previous': Config.NULL_API_RESPONSE
            }
        }
        all_skills = db.session.query(Skill).order_by(Skill.id_skill).all()
        self_index = -1
        for i in range(len(all_skills)):
            if all_skills[i].skill_name == self.skill_name:
                self_index = i
                break
        if self_index < len(all_skills) - 1 and self_index != -1:
            next_skill = Skill.query.filter_by(id_skill=all_skills[self_index + 1].id_skill).first()
            data['_links']['next'] = \
                url_for('api.get_skill_by_name', skill_name=next_skill.skill_name) if call == 'name' \
                else url_for('api.get_skill_by_id', skill_id=next_skill.id_skill)
        if self_index > 0 and self_index != -1:
            previous_skill = Skill.query.filter_by(id_skill=all_skills[self_index - 1].id_skill).first()
            data['_links']['previous'] = \
                url_for('api.get_skill_by_name', skill_name=previous_skill.skill_name) if call == 'name' \
                else url_for('api.get_skill_by_id', skill_id=previous_skill.id_skill)
        return data

    @staticmethod
    def insert_new_skill(skill_name, category_name,
                         is_shown=True):
        show = False
        if is_shown == 'true' or is_shown is True or is_shown == 1:
            show = True
        if Skill.query.filter_by(skill_name=skill_name).first() is None and len(skill_name) <= Config.MAX_SKILL_LENGTH:
            new_skill = Skill(skill_name, category_name, show)
            db.session.add(new_skill)
            db.session.commit()
            return True
        return False

    @staticmethod
    def delete_skill(skill_name):
        skill_to_be_deleted = Skill.query.filter_by(skill_name=skill_name).first()
        if skill_to_be_deleted is not None:
            db.session.delete(skill_to_be_deleted)
            db.session.commit()
            Category.delete_category((Category.query.filter_by(id_skill_cat=skill_to_be_deleted.id_cat).first()).
                                     category_name)
            return True
        return False

    @staticmethod
    def get_all_visible_skills():
        result_set, list_skills = [], []
        for c in Category.query.filter_by(is_shown=Config.VISIBLE_ON_FE):
            for s in c.skills:
                if s.skill_name is not None and s.skill_name != '' and s.is_shown is Config.VISIBLE_ON_FE:
                    list_skills.append(s)
            result_set.append({'category_name': c.category_name, 'skills': copy.copy(list_skills)})
            list_skills.clear()
        return result_set


class User(Timestamp, UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    username = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    preferred_language = db.Column(db.String(10), nullable=True)
    number_of_visits = db.Column(db.Integer, nullable=True)
    social_media = db.Column(db.String(30), nullable=True)
    welcome_email_sent = db.Column(db.Boolean, nullable=False)
    token = db.Column(db.String(Config.TOKEN_LENGTH), unique=True)
    token_expiration = db.Column(db.DateTime)

    def __init__(self, social_media, social_id, first_name, last_name, username, email, preferred_language,
                 visits=0):
        self.social_media = social_media
        self.social_id = social_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.preferred_language = preferred_language
        self.number_of_visits = visits
        self.welcome_email_sent = False
        self.set_new_token()

    def update_visits(self):
        self.number_of_visits += 1
        db.session.commit()

    def get_welcome_email_sent(self):
        return self.welcome_email_sent

    def set_welcome_email_sent(self, value):
        self.welcome_email_sent = value
        db.session.commit()

    def __repr__(self):
        return "<User: {self.social_media}, {self.social_id}, {self.first_name}, {self.last_name}, {self.username}, " \
               "{self.email}, {self.preferred_language}, {self.number_of_visits}, {self.welcome_email_sent}, " \
               "{self.token}, {self.token_expiration}, {self.updated}, {self.created}>".format(self=self)

    def __str__(self):
        return self.social_media + ':' + self.social_id

    # make the token invalid
    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    def token_is_expired(self):
        if self.token_expiration < datetime.utcnow():
            return True
        return False

    def set_new_token(self):
        self.token = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits,
                                            k=Config.TOKEN_LENGTH))
        self.token_expiration = datetime.utcnow() + timedelta(seconds=Config.TOKEN_EXPIRATION_IN_SEC)
        db.session.commit()

    @staticmethod
    def check_token(request):
        token = request.headers.get('Authorization', default=None, type=str)
        if token is None:
            return 404
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_is_expired():
            return 401
        return 200

    @staticmethod
    def delete_user_account(social_id):
        user_to_be_deleted = User.query.filter_by(social_id=social_id).first()
        if user_to_be_deleted is not None:
            db.session.delete(user_to_be_deleted)
            db.session.commit()
            return True
        return False

    @staticmethod
    def insert_new_user(social_media, social_id, first_name, last_name, username, email, preferred_language):
        if User.query.filter_by(social_id=social_id).first() is None:
            new_user = User(social_media, social_id, first_name, last_name, username, email, preferred_language)
            db.session.add(new_user)
            db.session.commit()
            return True
        return False


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # returns a User object based on its id, if not found, None
