#/usr/bin/env python
#-*- coding:utf8 -*-
import os
from flask import request,redirect,render_template,url_for,flash,Blueprint
from flask.ext.login import login_required
from app import settings
from app.core import app

from app.sales.model import Order,Shipment,Invoice


sales = Blueprint('sales', __name__,url_prefix='/sales',template_folder=os.path.join(settings.TEMPLATE_FOLDER,'sales'))


@sales.route('/order/')
@sales.route('/order/<int:page>/')
@login_required
def order(page = 1):
    pagination = Order.query.order_by(Order.id.desc()).paginate(page = page, per_page=10, error_out=False)
    return render_template('order/list.html',orders = pagination.items,pagination=pagination)


@sales.route('/order/view/<int:id>/')
@login_required
def order_view(id):
    order = Order.query.get_or_404(id)
    return render_template('order/view.html',order = order)


@sales.route('/shipment/')
@login_required
def shipment():
    return render_template('shipment.html')


@sales.route('/payment/')
@login_required
def payment():
    pass

@sales.route('/invoice/')
@login_required
def invoice():
    pass



app.register_blueprint(sales)
