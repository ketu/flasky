#/usr/bin/env python
#-*- coding:utf8 -*-
from datetime import datetime
import hashlib

from app import settings
from app.core import db




class Website(db.Document):

    name = db.StringField(required=True)
    code = db.StringField(required=True)
    link = db.StringField(required=True)
    type = db.StringField(choices = ('amazon','magento','ebay','aliexpress','other'))
    config = db.StringField()



    def __unicode__(self):
        return self.name