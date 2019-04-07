import datetime
import logging
import string
import os


basedir = os.path.abspath(os.path.dirname(__file__))  # project folder


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('MYSQL_DATABASE_URL') or os.environ.get('SQLITE_DATABASE_URL') \
                              or 'sqlite:///' + os.path.join(basedir, 'skills.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FORBIDDEN_CHARACTERS = string.punctuation
    VISIBLE_ON_FE = True
    EMPTY = 0
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': os.environ.get('FB_ID') or None,
            'secret': os.environ.get('FB_SECRET') or None
        },
        'linkedin': {
            'id': os.environ.get('LI_ID') or None,
            'secret': os.environ.get('LI_SECRET') or None
        }
    }
    LINKEDIN_PROFILE_INFO_API_LINK = 'https://api.linkedin.com/v2/me'
    LINKEDIN_SCOPE = 'r_liteprofile'  # r_basicprofile has been discontinued for not-registered developers
    FACEBOOK_SCOPE = 'email'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or None
    MAIL_PORT = os.environ.get('MAIL_PORT') or 25
    MAIL_USE_TSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or None
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or None
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME') or None
    WELCOME_EMAIL_MSG = """Hello <strong>{0}</strong>,<br>
welcome to my personal site :) Since you have registered, you can now find here a bit more about myself 
and especially about my profession and profession interests. I have also added some information about my current 
technical skills, so if you are interested in what I can do in the field of IT, please read on.<br>
If you want to to leave me a message, you can certainly do so after you have read my page and my LinkedIn profile. 
This app/website is smart enough to figure it out :)<br>
Best regards<br>
Pavel"""
    MAIL_NAME = 'Pavel Saman'
    MAIL_WELCOME_SUBJECT = 'Welcome - Pavel Saman'
    FALLBACK_ADMIN_EMAIL = os.environ.get('FALLBACK_ADMIN_EMAIL')
    BYE_EMAIL_MSG = """Thank you for being part of my website.<br>
All your information has been deleted right after sending this email.<br>
You can come back at any time in the future.<br>
Best regards<br>
Pavel
    """
    MAIL_BYE_SUBJECT = 'Bye - Pavel Saman'
    ERROR_EMAIL_SUBJECT = '!!! Error on your server !!!'
    LOG_DIRECTORY = 'logs'
    LOG_FILE_NAME = 'logs/skills.log'
    LOG_LEVEL_EMAILS = logging.ERROR
    LOG_LEVEL_FILES = logging.INFO
    LOG_IN_REQUIRED_MESSAGE = 'Please log in to go further.'
    LOG_IN_START_VIEW = 'main.index'
    LOG_IN_REFRESH_VIEW = 'main.index'
    REMEMBER_COOKIE_NAME = 'skills'
    REMEMBER_COOKIE_DURATION = datetime.timedelta(days=7)
    SESSION_PROTECTION = 'strong'
    TOKEN_EXPIRATION_IN_SEC = 86400  # 1 day in seconds
    TOKEN_LENGTH = 32
    NULL_API_RESPONSE = 'NaN'
    MIN_SKILL_LENGTH = 2
    MIN_CATEGORY_LENGTH = 2
    MAX_SKILL_LENGTH = 30
    MAX_CATEGORY_LENGTH = 30
    MAX_BYTES_LOG_FILE = 10240
    MAX_LOG_FILES = 5
    API_DELETION_SUCCESS = {'response': 'OK'}


class ErrorMessages:
    SKILL_TOO_MANY_CHARS = 'The length has to be at least 2 characters, maximum 30 characters.'
    SKILL_INVALID_CHARACTERS = 'The field contains invalid characters.'
    SKILL_REQUIRED = 'Skill field is required.'
    SKILL_NOT_UNIQUE = 'Entered skill is not unique.'
    CATEGORY_TOO_MANY_CHARS = 'The length has to be at least 2 characters, maximum 30 characters.'
    CATEGORY_INVALID_CHARACTERS = 'The field contains invalid characters.'
    CATEGORY_REQUIRED = 'Category field is required.'
    CATEGORY_NOT_UNIQUE = 'Entered category is not unique.'
    UNSUCCESSFUL_AUTHORIZATION = 'Loggin was not completed.'
    UNSUCCESSFUL_NEW_USER = 'New user was not created.'
    USER_LOGOUT = 'You have been logged out.'
    USER_DELETION = 'Your account has been deleted.'
    API_CATEGORY_INSERT_ERROR = 'Category cannot be added, it might already exist or the name is too long.'
    API_SKILL_INSERT_ERROR = 'Skill cannot be added, it might already exist or the name is too long.'
    API_FORMAT_NOT_ALLOWED = 'This format is not allowed.'
    API_DELETE_SKILL_FAILURE = 'Skill cannot be deleted. Check its name again.'
    API_DELETE_CATEGORY_FAILURE = 'Category cannot be deleted. Check its name again and that the category is empty.'
    API_SKILL_NAME_ERROR = 'Skill name not allowed.'
    API_CATEGORY_NAME_ERROR = 'Category name not allowed.'
