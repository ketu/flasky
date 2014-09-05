#/usr/bin/env python
#-*- coding:utf8 -*-
from flask import render_template,redirect,url_for,flash
from flask.views import View,MethodView

from app.core import lm
from app.core.views import ViewMixin


from .model import User
from .forms import LoginForm



@lm.user_loader
def load_user(id):
    return User.query.get(int(id))





class LoginView(MethodView,ViewMixin):
    def get(self):
        form = LoginForm()
        return render_template(self.template_name,form=form)
    def post(self):
        form = LoginForm()
        if form.validate_on_submit():

            flash('Login requested for OpenID="' + form.email.data + '", remember_me=' + str(form.remember.data))
            return redirect(url_for('accounts.login'))
        return render_template(self.template_name,form=form)
        #return redirect(url_for('dashboard'))

class ProfileView(MethodView,ViewMixin):
    pass



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
