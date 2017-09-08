import os
from flask import Flask
from sqlalchemy import DDL, event
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, \
    MAIL_PASSWORD
from app.momentjs import momentjs

app = Flask(__name__)
app.config.from_object('config')
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '1884432745103765',
        'secret': '90f5ffdf9e99841d0c9d7f903e18a51d'
    },
    'google': {
        'id': '176592896048-ver8bjf3errq8t0rcpe6htre8ol5tbqq.apps.googleusercontent.com',
        'secret': 'y46GFKpvW9x2HQ27MN-F2fdd'
    }
}
app.config.update(TEMPLATES_AUTO_RELOAD=True)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'facebook_authorize'
login_manager.login_message = 'Please log in to access this page.'

mail = Mail(app)

if not app.debug and MAIL_SERVER != '':
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT),
                               'no-reply@' + MAIL_SERVER, ADMINS,
                               'gs-cookies failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

if not app.debug and os.environ.get('HEROKU') is None:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/gs-cookies.log', 'a',
                                       1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('gs-cookies startup')

#TODO Clean this up
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-unit-testing
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')

app.jinja_env.globals['momentjs'] = momentjs

from app import views, models
