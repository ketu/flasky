#/usr/bin/env python
#-*- coding:utf8 -*-
import os
from flask import request,redirect,render_template,url_for,flash,Blueprint
from flask.ext.login import login_required
from flask.ext.babel import gettext as _
from app import settings
from app.core import app
from .model import Category,Product,ProductGallery
from .forms import CategoryForm

catalog = Blueprint('catalog', __name__,url_prefix='/catalog',template_folder=os.path.join(settings.TEMPLATE_FOLDER,'catalog'))


@catalog.route('/category/')
@login_required
def category(page=1):
    pagination = Category.objects.order_by("-id").paginate(page = page, per_page=10)
    return render_template('category/list.html', categories=pagination.items, pagination=pagination)


@catalog.route('/category/add/',endpoint='add_category',methods=['GET','POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():

        category = Category(
                    parent=form.parent.data,
                    name = form.name.data,
                    )
        category.save()
        flash(_('Category add successful'))
        return redirect(url_for('catalog.category'))


    return render_template('add.html',form=form)



@catalog.route('/product/')
@login_required
def product():
    return render_template('product.html')



app.register_blueprint(catalog)
