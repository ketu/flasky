#/usr/bin/env python
#-*- coding:utf8 -*-
from datetime import datetime
import hashlib

from app import settings
from app.core import db




class Website(db.Document):

    name = db.StringField(required=True)
    code = db.StringField(required=True, unique=True)
    link = db.StringField(required=True)
    type = db.StringField(choices = settings.API_TYPE)
    created_at = db.DateTimeField(default=datetime.now)
    config = db.DictField()



    def __unicode__(self):
        return self.name