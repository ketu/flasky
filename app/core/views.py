#/usr/bin/env python
#-*- coding:utf8 -*-

from flask import request,redirect,render_template,url_for,flash,Blueprint
from flask.ext.login import login_required,current_user

from app.core import app

class ViewMixin(object):
    def __init__(self,template = None):
        if template :
            self.template_name = template



@app.route('/')
@login_required
def index():
    return redirect(url_for('system.dashboard'))
