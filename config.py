# -*- coding: utf8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))
DIRNAME = os.path.dirname(__file__)

CSRF_ENABLED = True
SECRET_KEY = 'my-big-fat-code'
TEMPLATES_AUTO_RELOAD = True

# if os.environ.get('DATABASE_URL') is None:
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# else:
#     SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_DATABASE_URI = 'mysql://gs_cookies:gs_cookies@localhost/gs_cookies'

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True

# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'jeffrey.blasius@gmail.com'
MAIL_PASSWORD = 'ekcjotvrxkppvugt'

# administrator list
ADMINS = ['jeffrey.blasius@gmail.com']

SERVICE_KEY = os.path.join(basedir, 'service_key.json')
