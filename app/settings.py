#/usr/bin/env python
#-*- coding:utf8 -*-
import os

DEBUG = True

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


CSRF_ENABLED = True

SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O3<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

#SQLALCHEMY_DATABASE_URI = 'sqlite:///'+SITE_ROOT+'/angoo.db'

SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/flask'

TEMPLATE_FOLDER = SITE_ROOT + '/templates'

STATIC_FOLDER = SITE_ROOT + '/static'

INSTALLED_APPLICATION = (
    'accounts',
    'dashboard',
    'customers',
    'search',
    'catalog',
    'sales'
)


API_TYPE = ('amazon','magento','ebay','aliexpress','other')

LANGUAGES = {
    'en': 'English',
    'cn': 'Chinese'
}

LIST_PER_PAGE = 10

SQLALCHEMY_ECHO = False

SQLALCHEMY_RECORD_QUERIES = True

#FLask-WFT
#Flask-Migrate
#Flask-Script
#Flask-Security
#Flask-MongoAlchemy
#Flask-SQLAlchemy
#Flask-Bootstrap
#Flask-Babel