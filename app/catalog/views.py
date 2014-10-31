#/usr/bin/env python
#-*- coding:utf8 -*-
import os
from flask import request,redirect,render_template,url_for,flash,Blueprint
from flask.ext.login import login_required
from app import settings
from app.core import app


catalog = Blueprint('catalog', __name__,url_prefix='/catalog',template_folder=os.path.join(settings.TEMPLATE_FOLDER,'catalog'))



@catalog.route('/category/')
@login_required
def category():
    return render_template('category.html')


@catalog.route('/product/')
@login_required
def product():
    return render_template('product.html')



app.register_blueprint(catalog)
