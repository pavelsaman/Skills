from skills.models import User
from flask import redirect, url_for, flash
from skills.auth.emails import send_welcome_email, send_bye_email
from flask_login import current_user, login_user, logout_user, login_required
from skills.auth.oauth import OAuthSignIn
from config import ErrorMessages
from skills.auth import bp


# after a user presses Log in with Facebook, this function handles it
@bp.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('content.index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@bp.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_media, social_id, first_name, last_name, username, email, preferred_language = oauth.callback()
    if (social_id is None and social_media == 'facebook') or (last_name is None and social_media == 'linkedin'):
        flash(ErrorMessages.UNSUCCESSFUL_AUTHORIZATION)
        return redirect(url_for('main.index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        if not User.insert_new_user(social_media, social_id, first_name, last_name, username, email,
                                    preferred_language):
            flash(ErrorMessages.UNSUCCESSFUL_NEW_USER)
            return redirect(url_for('main.index'))
        user = User.query.filter_by(social_id=social_id).first()
    login_user(user, True)
    user.update_visits()
    if user.email is not None and user.first_name is not None and not user.get_welcome_email_sent():
        send_welcome_email(user.first_name, user.email)
        user.set_welcome_email_sent(True)
    return redirect(url_for('content.index'))


@bp.route('/auth/logout/', methods=['GET'])
@bp.route('/auth/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash(ErrorMessages.USER_LOGOUT)
    return redirect(url_for('main.index'))


@bp.route('/auth/delete/account/', methods=['GET'])
@bp.route('/auth/delete/account', methods=['GET'])
@login_required
def delete_account():
    user_to_be_deleted = current_user.social_id
    if current_user.email is not None:
        send_bye_email(current_user.email)
    logout_user()
    User.delete_user_account(user_to_be_deleted)
    flash(ErrorMessages.USER_DELETION)
    return redirect(url_for('main.index'))
