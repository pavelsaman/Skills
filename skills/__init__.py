from logging.handlers import RotatingFileHandler
from logging.handlers import SMTPHandler
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from flask import Flask
import logging
import os


db = SQLAlchemy()
lm = LoginManager()
mail = Mail()


def create_app(config_class=Config, debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.config.from_object(config_class)
    app.app_context().push()
    mail.init_app(app)
    lm.init_app(app)
    lm.login_view = app.config['LOG_IN_START_VIEW']
    lm.login_message = app.config['LOG_IN_REQUIRED_MESSAGE']
    lm.refresh_view = app.config['LOG_IN_REFRESH_VIEW']
    lm.session_protection = app.config['SESSION_PROTECTION']
    from skills.models import init_db
    db.init_app(app)
    init_db()
    # Blueprint registration
    from skills.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    from skills.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    from skills.main import bp as main_bp
    app.register_blueprint(main_bp)
    from skills.content import bp as content_bp
    app.register_blueprint(content_bp)
    from skills.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    # production
    if not app.debug:  # only in debug
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TSL']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr=app.config['MAIL_USERNAME'],
                toaddrs=app.config['FALLBACK_ADMIN_EMAIL'],
                subject=app.config['ERROR_EMAIL_SUBJECT'],
                credentials=auth, secure=secure)
            mail_handler.setLevel(app.config['LOG_LEVEL_EMAILS'])  # sending only errors by email
            app.logger.addHandler(mail_handler)
            if not os.path.exists(app.config['LOG_DIRECTORY']):
                os.mkdir(app.config['LOG_DIRECTORY'])
            file_handler = RotatingFileHandler(app.config['LOG_FILE_NAME'], maxBytes=app.config['MAX_BYTES_LOG_FILE'],
                                               backupCount=app.config['MAX_LOG_FILES'])
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(app.config['LOG_LEVEL_FILES'])  # I'll see every server restart as well
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Startup')
    return app
