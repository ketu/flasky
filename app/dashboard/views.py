#/usr/bin/env python
#-*- coding:utf8 -*-
from flask import request,redirect,render_template,url_for,flash,Blueprint,g
from flask.ext.login import login_required,current_user
from app.core import app

system = Blueprint('system', __name__, url_prefix='/system')

@system.route('/')
@login_required
def dashboard():
    flash("Login in lasdf")
    return render_template('dashboard.html',title='Dashboard')


@system.route('/message/')
@login_required
def message():
    return render_template('message.html')


@system.route('/alerts/')
@login_required
def alerts():
    return render_template('alerts.html')


@system.route('/tasks/')
@login_required
def tasks():
    return render_template('tasks.html')

@system.route('/settings/',methods = ['GET','POST'])
@login_required
def settings():
    return render_template('settings.html')

app.register_blueprint(system)