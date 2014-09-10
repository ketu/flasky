#/usr/bin/env python
#-*- coding:utf8 -*-
from flask import request,redirect,render_template,url_for,flash,Blueprint
from flask.views import View,MethodView

from flask.ext.login import login_required

from app.core import app
system = Blueprint('system', __name__, url_prefix='/system')



@system.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')


@system.route('/message/')
def message():
    return render_template('message.html')


@system.route('/alerts/')
def alerts():
    return render_template('alerts.html')


@system.route('/tasks/')
def tasks():
    return render_template('tasks.html')

@system.route('/settings/',methods = ['GET','POST'])
def settings():
    return render_template('settings.html')

app.register_blueprint(system)