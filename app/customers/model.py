#/usr/bin/env python
#-*- coding:utf8 -*-
from datetime import datetime
from app.core import db
from app.dashboard.model import Website


class Customer(db.Document):
    website = db.ReferenceField("Website")
    group = db.ReferenceField("Group")
    email = db.StringField(required=True,unique=True)
    firstname = db.StringField()
    lastname = db.StringField()
    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()

class Group(db.Document):
    name = db.StringField(required=True,unique=True)

class Address(db.Document):
    customer = db.ReferenceField("Customer")
    firstname = db.StringField()
    lastname = db.StringField()
    country = db.StringField()
    region = db.StringField()
    region_id = db.StringField()
    postcode = db.StringField()
    city = db.StringField()
    street = db.StringField()
    telephone = db.StringField()
    fax = db.StringField()
    company = db.StringField()
    address_type = db.StringField(choices = ('shipping','billing'))
    created_at = db.DateTimeField(default=datetime.now)