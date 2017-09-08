from flask import Flask, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
from app import app
"""
    google example
    ~~~~~~~~~~~~~~
    This example is contributed by Bruno Rocha
    GitHub: https://github.com/rochacbruno

    https://github.com/lepture/flask-oauthlib/blob/master/example/google.py
"""
 
# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
credentials = app.config['OAUTH_CREDENTIALS']['google']
# REDIRECT_URI = '/oauth2callback'  # one of the Redirect URIs from Google APIs console
app.config['GOOGLE_ID'] = credentials['id']
app.config['GOOGLE_SECRET'] = credentials['secret']
# app.debug = True
# app.secret_key = 'development'
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


# @app.route('/')
# def index():
#     if 'google_token' in session:
#         me = google.get('userinfo')
#         return jsonify({"data": me.data})
#     return redirect(url_for('login'))


# @app.route('/login')
# def login():
#     return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    return jsonify({"data": me.data})


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


# if __name__ == '__main__':
