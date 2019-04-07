from flask import current_app, url_for, request, redirect
from rauth import OAuth2Service  # there is also version 1
from config import Config
import json


class OAuthSignIn:
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        # loading sensitive info from Config
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    # initiation of the authentication process, the user needs to be redirected to the provider's web site
    def authorize(self):
        raise NotImplemented

    # when the authentication is done, the provider will redirect the user back, it'll be handled here
    def callback(self):
        raise NotImplemented

    # this is a URL that the provider needs to redirect to, each provider gets only its dedicated route based on
    # provider's name here
    def get_callback_url(self):
        return url_for('auth.oauth_callback', provider=self.provider_name, _external=True)

    @classmethod
    def get_provider(cls, provider_name):
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name]


class FacebookSignIn(OAuthSignIn):

    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        # rauth
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    # initiation of the authentication process, the user needs to be redirected to the provider's web site
    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope=Config.FACEBOOK_SCOPE,
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    # when the authentication is done, the provider will redirect the user back, it'll be handled here
    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None, None, None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=decode_json
        )
        user = oauth_session.get('me?fields=id,first_name,last_name,email,name_format').json()
        return (  # return FB data from the json
            'facebook',
            user['id'],
            user['first_name'],
            user['last_name'],
            user.get('email').split('@')[0],
            user.get('email'),
            None
        )


class LinkedInSignIn(OAuthSignIn):

    def __init__(self):
        super(LinkedInSignIn, self).__init__('linkedin')
        # rauth
        self.service = OAuth2Service(
            name='linkedin',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://www.linkedin.com/oauth/v2/authorization',
            access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
            base_url='https://www.linkedin.com/'
        )

    # initiation of the authentication process, the user needs to be redirected to the provider's web site
    def authorize(self):
        return redirect(self.service.get_authorize_url(
            response_type='code',
            scope=Config.LINKEDIN_SCOPE,
            redirect_uri=self.get_callback_url())
        )

    # when the authentication is done, the provider will redirect the user back, it'll be handled here
    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None, None, None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=decode_json
        )
        user = oauth_session.get(Config.LINKEDIN_PROFILE_INFO_API_LINK).json()
        return (
            'linkedin',
            user['id'],
            [value for key, value in user['firstName']['localized'].items()][0],
            [value for key, value in user['lastName']['localized'].items()][0],
            None,
            None,
            user['lastName']['preferredLocale']['language'] + '_' + user['lastName']['preferredLocale']['country']
        )
