#/usr/bin/env python
#-*- coding:utf8 -*-
from flask import render_template,redirect,url_for
from flask.views import View,MethodView

from flask.ext.login import login_required
from app.core.views import ViewMixin

class DashboardView(View,ViewMixin):
    decorators = [login_required]

    def dispatch_request(self):
        return render_template(self.template_name)

class MessageView(View,ViewMixin):
    decorators = [login_required]
    def dispatch_request(self):
        return render_template(self.template_name)

class AlertsView(View,ViewMixin):
    decorators = [login_required]
    def dispatch_request(self):
        return render_template(self.template_name)

class TasksView(View,ViewMixin):
    decorators = [login_required]
    def dispatch_request(self):
        return render_template(self.template_name)


class SearchView(View,ViewMixin):
    decorators = [login_required]
    def dispatch_request(self):
        return render_template(self.template_name)

class SettingsView(MethodView,ViewMixin):
    decorators = [login_required]
    def get(self):
        return render_template(self.template_name)

    def post(self):
        return render_template(self.template_name)

