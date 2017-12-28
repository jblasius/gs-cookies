from flask import current_app, redirect, url_for, request, session
from rauth import OAuth2Service
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from app.models import *
import json

"""
Facebook implementation based on
http://www.vertabelo.com/blog/technical-articles/how-to-store-authentication-data-in-a-database-part-4-implementing-the-login-with-facebook-button-in-python
"""
def external_auth():
    oauth = FacebookSignIn()
    facebook_id, email, first_name, last_name = oauth.callback()
    if facebook_id is None:
        flash('Authentication failed')
        # change the status of async operation for 'error'
        status_error = AsyncOperationStatus.query.filter_by(code='error').first()
        async_operation = AsyncOperation.query.filter_by(id=session['async_operation_id']).first()
        async_operation.async_operation_status_id = status_error.id
        db.session.add(async_operation)
        db.session.commit()
        return redirect(url_for('error'))

    # retrieve the user data from the database
    # print 'facebook_id=' + facebook_id
    # print 'email=' + email
    # print 'first_name=' + first_name
    # print 'last_name=' + last_name

    user = User.query.filter_by(social_id=facebook_id).first()

    # if the user is new, we store theirs credentials in user_profile table
    if not user:
        user = User(social_id=facebook_id, email=email, first_name=first_name, last_name=last_name)
        print 'user variable set'
        db.session.add(user)
        db.session.commit()

    # change the status of the async operation for 'ok' and insert the value of the user id
    # to the async_operation table
    status_ok = AsyncOperationStatus.query.filter_by(code='ok').first()
    async_operation = AsyncOperation.query.filter_by(id=session['async_operation_id']).first()
    async_operation.async_operation_status_id = status_ok.id
    async_operation.user_profile_id = user.id
    db.session.add(async_operation)
    db.session.commit()


class FacebookSignIn(object):

    def __init__(self):
        credentials = app.config['OAUTH_CREDENTIALS']['facebook']
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='public_profile,email',
            display='popup',
            response_type='code',
            redirect_uri=self.get_callback_url()
        ))

    def get_callback_url(self):
        return url_for('show_preloader_start_authentication', _external=True)

    def callback(self):
        if 'code' not in request.args:
            return None, None, None, None
        oauth_session = self.service.get_auth_session( \
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=json.loads)
        me = oauth_session.get('me?fields=id,email,first_name,last_name').json()
        return (
            me['id'],
            me.get('email'),
            me.get('first_name'),
            me.get('last_name')
        )
