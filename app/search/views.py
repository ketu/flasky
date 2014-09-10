#/usr/bin/env python
#-*- coding:utf8 -*-
from flask import request,redirect,render_template,url_for,flash,Blueprint
from flask.views import View,MethodView
from app.core import app

@app.route('/search/')
def search():
    return render_template('dashboard.html')
