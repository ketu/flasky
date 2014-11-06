#/usr/bin/env python
#-*- coding:utf8 -*-
import os
from flask import request,redirect,render_template,url_for,flash,Blueprint
from flask.ext.login import login_required
from flask.ext.babel import gettext as _
from app import settings
from app.core import app
from .model import Category,Product,ProductGallery
from .forms import CategoryForm, ProductForm

#from app.dashboard.model import Website

catalog = Blueprint('catalog', __name__,url_prefix='/catalog',template_folder=os.path.join(settings.TEMPLATE_FOLDER,'catalog'))


@catalog.route('/category')
@catalog.route('/category/<int:page>')
@login_required
def category(page=1):
    pagination = Category.objects.order_by("-id").paginate(page = page, per_page=10)
    return render_template('category/list.html', categories=pagination.items, pagination=pagination)


@catalog.route('/category/import/<website>',endpoint='import_category')
@login_required
def import_category(website):
    pass
    #website = Website.objects.get_or_404(id=website)



@catalog.route('/category/add/',endpoint='add_category',methods=['GET','POST'])
@catalog.route('/category/edit/<id>',endpoint='edit_category',methods=['GET','POST'])
@login_required
def add_category(id = None):
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
                    parent=form.parent.data,
                    name = form.name.data,
                    )
        category.save()
        flash(_('Category add successful'))
        return redirect(url_for('catalog.category'))


    return render_template('category/add.html',form=form, breadcrumb=['Home','Category'])



@catalog.route('/product')
@catalog.route('/product/<int:page>')
@login_required
def product(page=1):
    pagination = Product.objects.order_by("-id").paginate(page = page, per_page=10)
    return render_template('product/list.html', products=pagination.items, pagination=pagination)



@catalog.route('/product/add', endpoint='add_product',methods=['GET','POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        pass

        flash(_('Product add successful'))
        return redirect(url_for('catalog.category'))

    return  render_template('product/add.html',form=form)





app.register_blueprint(catalog)
