#/usr/bin/env python
#-*- coding:utf8 -*-

from flask import redirect,g,url_for,session


class ViewMixin(object):
    def __init__(self,template = None):
        if template :
            self.template_name = template

