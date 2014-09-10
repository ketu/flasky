#/usr/bin/env python
#-*- coding:utf8 -*-
import os
from flask import request,redirect,render_template,url_for,flash,Blueprint
from flask.ext.login import login_required
from app import settings
from app.core import app


customers = Blueprint('customers', __name__,url_prefix='/customers',template_folder=os.path.join(settings.TEMPLATE_FOLDER,'customers'))



@customers.route('/')
@login_required
def index():
    return render_template('dashboard.html')


@customers.route('/view/<int:id>')
@login_required
def view():
    return render_template('message.html')



app.register_blueprint(customers)
