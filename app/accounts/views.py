#/usr/bin/env python
#-*- coding:utf8 -*-
from flask import render_template,redirect,url_for
from flask.views import View,MethodView

from app.core import lm
from app.core.views import ViewMixin
from .model import User



@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


class ProfileView(MethodView,ViewMixin):
    pass

class LoginView(MethodView,ViewMixin):
    def get(self):
        return render_template(self.template_name)
    def post(self):
        return redirect(url_for('dashboard'))

class RegisterView(MethodView,ViewMixin):
    def get(self):
        pass
    def post(self):
        pass

class LogoutView(MethodView,ViewMixin):
    def get(self):
        pass
    def post(self):
        pass
