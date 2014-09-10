#/usr/bin/env python
#-*- coding:utf8 -*-
import os
from flask import request,redirect,render_template,url_for,flash,Blueprint

from app import settings
from app.core import app


sales = Blueprint('sales', __name__,url_prefix='/sales',template_folder=os.path.join(settings.TEMPLATE_FOLDER,'sales'))



@sales.route('/login/',methods=['GET','POST'])

@sales.route('/order/')
def order():
    return render_template('dashboard.html')


@sales.route('/shipment/')
def shipment():
    return render_template('message.html')



app.register_blueprint(sales)
