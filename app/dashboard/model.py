#/usr/bin/env python
#-*- coding:utf8 -*-
from datetime import datetime
import hashlib

from app import settings
from app.core import db




class Website(db.Model):
    __tablename__ = 'website'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(254))
    code = db.Column(db.String(32))
    link = db.Column(db.String(254))
    type = db.Column(db.Enum('amazon','magento','ebay','aliexpress','other'))
    config = db.Column(db.Text,nullable=True)
