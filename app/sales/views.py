#/usr/bin/env python
#-*- coding:utf8 -*-
from flask import render_template,redirect,url_for
from flask.views import View,MethodView
from app.core.views import ViewMixin


class OrderView(MethodView,ViewMixin):
    pass

class CategoryView(MethodView,ViewMixin):

    def get(self):
        return render_template(self.template_name)


    def post(self):
        return redirect(url_for('dashboard'))




class ProductView(MethodView,ViewMixin):

    def get(self):
        pass

    def post(self):
        pass


class ShipmentView(MethodView,ViewMixin):

    def get(self):
        pass

    def post(self):
        pass
