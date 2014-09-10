#/usr/bin/env python
#-*- coding:utf8 -*-
import os

DEBUG = True

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


CSRF_ENABLED = True

SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O3<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

SQLALCHEMY_DATABASE_URI = 'sqlite:///'+SITE_ROOT+'/angoo.db'

TEMPLATE_FOLDER = SITE_ROOT + '/templates'
STATIC_FOLDER = SITE_ROOT + '/static'

INSTALLED_APPLICATION = (
    'dashboard',
    'accounts',
    'search',
    'catalog',
    'customers',
    'sales'
)


LANGUAGES = {
    'en': 'English',
    'cn': 'Chinese'
}

#FLask-WFT
#Flask-Migrate
#Flask-Script
#Flask-Security
#Flask-MongoAlchemy
#Flask-SQLAlchemy
#Flask-Bootstrap
#Flask-Babel