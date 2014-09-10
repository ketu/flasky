#/usr/bin/env python
#-*- coding:utf8 -*-

from flask import Flask, request
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap
from flask.ext.babel import Babel
from flask.ext.sqlalchemy import SQLAlchemy

from app import settings

app = Flask(__name__,template_folder=settings.TEMPLATE_FOLDER,static_folder=settings.STATIC_FOLDER)

app.config.from_object(settings)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


bootstrap = Bootstrap(app)
babel = Babel(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'accounts.login'


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(settings.LANGUAGES.keys())
