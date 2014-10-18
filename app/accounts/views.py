#/usr/bin/env python
#-*- coding:utf8 -*-
import os
from flask import request,redirect,render_template,url_for,flash,Blueprint
from flask.ext.login import login_required,login_user,logout_user



from app import settings
from app.core import login_manager,app,db


from .model import User
from .forms import LoginForm,RegisterForm




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

@account.route('/register/',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()



        flash('A confirmation email has been sent to you by email. '+token)
        return redirect(url_for('accounts.login'))

    return render_template('register.html',form=form)



@account.route('/profile/')
@login_required
def profile():
    return render_template('message.html')


@account.route('/logout/')
@login_required
def logout():

    logout_user()
    return redirect(url_for('accounts.login'))


app.register_blueprint(account)
