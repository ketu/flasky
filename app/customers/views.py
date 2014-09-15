#/usr/bin/env python
#-*- coding:utf8 -*-
import os
from flask import request,redirect,render_template,url_for,flash,Blueprint,current_app
from flask.ext.login import login_required
from flask.ext.babel import gettext as _


from app import settings
from app.core import app,db
from app.customers.model import Customer

from app.customers.forms import CustomerForm


customers = Blueprint('customers', __name__,url_prefix='/customers',template_folder=os.path.join(settings.TEMPLATE_FOLDER,'customers'))



@customers.route('/')
@customers.route('/list/<int:page>/')
@login_required
def index(page = 1):
    #page = (Customer.query.count() - 1) / current_app.config['LIST_PER_PAGE'] + 1
    pagination = Customer.query.order_by(Customer.id.desc()).paginate(page = page, per_page=10, error_out=False)
    return render_template('customers.html',customers = pagination.items,pagination=pagination)


@customers.route('/add/', methods = ['GET','POST'])
@login_required
def add():
    form = CustomerForm()
    if form.validate_on_submit():

        user = Customer(email=form.email.data,
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    website_id = form.website_id.data.id,
                    group_id = form.group_id.data
                    )

        db.session.add(user)
        db.session.commit()
        flash(_('Customer add successful'))
        return redirect(url_for('customers.index'))


    return render_template('add.html',form=form)

@customers.route('/view/<int:id>')
@login_required
def view():
    return render_template('message.html')



app.register_blueprint(customers)
