from flask_mail import Message
from flask import current_app
from threading import Thread
from config import Config
from skills import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_welcome_email(first_name, recipient):
    msg = Message(subject=Config.MAIL_WELCOME_SUBJECT,
                  sender=(Config.MAIL_NAME, Config.MAIL_USERNAME),
                  recipients=[recipient if recipient != Config.ADMIN_EMAIL else Config.FALLBACK_ADMIN_EMAIL])
    msg.html = Config.WELCOME_EMAIL_MSG.format(first_name)
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_bye_email(recipient):
    msg = Message(subject=Config.MAIL_BYE_SUBJECT,
                  sender=(Config.MAIL_NAME, Config.MAIL_USERNAME),
                  recipients=[recipient if recipient != Config.ADMIN_EMAIL else Config.FALLBACK_ADMIN_EMAIL])
    msg.html = Config.BYE_EMAIL_MSG
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
