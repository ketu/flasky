#/usr/bin/env python
#-*- coding:utf8 -*-
import os
from flask import request,redirect,render_template,url_for,flash,Blueprint
from flask.views import View,MethodView

from flask.ext.login import login_required,login_user,logout_user

from app import settings
from app.core import login_manager,app
from app.core.views import ViewMixin

from .model import User
from .forms import LoginForm


account = Blueprint('accounts', __name__,url_prefix='/accounts',template_folder=os.path.join(settings.TEMPLATE_FOLDER,'accounts'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@account.route('/login/',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember.data)
            return redirect(request.args.get('next') or url_for('system.dashboard'))
        flash('Invalid username or password.')
    return render_template('login.html',form=form)

@account.route('/register/')
def register():
    return render_template('dashboard.html')


@account.route('/profile/')
def profile():
    return render_template('message.html')


@account.route('/logout/')
def logout():
    return render_template('alerts.html')




app.register_blueprint(account)

"""
class LoginView(MethodView,ViewMixin):
    def get(self):
        form = LoginForm()
        return render_template(self.template_name,form=form)
    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.verify_password(form.password.data):
                login_user(user, form.remember.data)
                return redirect(request.args.get('next') or url_for('system.dashboard'))
            flash('Invalid username or password.')
            return render_template(self.template_name,form=form)
        #return redirect(url_for('dashboard'))
"""
