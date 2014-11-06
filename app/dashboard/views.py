#/usr/bin/env python
#-*- coding:utf8 -*-
import os
from flask import request,redirect,render_template,url_for,flash,Blueprint,g
from flask.ext.login import login_required,current_user
from flask.ext.babel import gettext as _
from app import settings
from app.core import app
from .model import Website
from .forms import WebsiteForm
system = Blueprint('system', __name__, url_prefix='/system', template_folder=os.path.join(settings.TEMPLATE_FOLDER,'system'))

@system.route('/')
@login_required
def dashboard():
    flash("Login in lasdf")
    return render_template('dashboard.html',title='Dashboard')


@system.route("/website/delete/<id>", endpoint='delete_website')
@login_required
def delete_website(id):
    website = Website.objects.get_or_404(id=id)
    website.delete()
    flash(_('Website deleted successful'))
    return redirect(url_for('system.website'))

@system.route("/website", methods=['GET','POST'])
@login_required
def website():
    websites = Website.objects.all()
    form = WebsiteForm()
    if form.validate_on_submit():


        config = {
            'api':form.key.data,
            'secret': form.secret.data
        }

        website = Website(
                    code=form.code.data,
                    name = form.name.data,
                    type = form.type.data,
                    link = form.link.data,
                    config = config,
                    #key = form.key.data,
                    #secret = form.secret.data,
                    )
        website.save()
        flash(_('Website add successful'))
        return redirect(url_for('system.website'))

    return render_template('website.html',title=_('Website'), websites=websites, form=form)


@system.route('/message')
@login_required
def message():
    return render_template('message.html')


@system.route('/alerts')
@login_required
def alerts():
    return render_template('alerts.html')


@system.route('/tasks')
@login_required
def tasks():
    return render_template('tasks.html')

@system.route('/settings',methods = ['GET','POST'])
@login_required
def settings():
    return render_template('settings.html')

app.register_blueprint(system)