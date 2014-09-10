#/usr/bin/env python
#-*- coding:utf8 -*-
import os
from flask import request,redirect,render_template,url_for,flash,Blueprint

from app import settings
from app.core import app


catalog = Blueprint('catalog', __name__,url_prefix='/catalog',template_folder=os.path.join(settings.TEMPLATE_FOLDER,'catalog'))





@catalog.route('/category/')
def category():
    return render_template('dashboard.html')


@catalog.route('/product/')
def product():
    return render_template('message.html')



app.register_blueprint(catalog)
