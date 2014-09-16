#/usr/bin/env python
#-*- coding:utf8 -*-
from datetime import datetime

from app.core import db
from app.dashboard.model import Website


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    website_id = db.Column(db.Integer, db.ForeignKey('website.id'))
    website = db.relationship("Website", uselist=False, backref="customer", lazy="joined")
    group_id = db.Column(db.Integer, db.ForeignKey('customer_group.id'))
    group = db.relationship("Group", uselist=False, backref="customer", lazy="joined")
    email = db.Column(db.String(254), unique=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    default_shipping = db.Column(db.Integer, db.ForeignKey('customer_address.id'))
    default_billing = db.Column(db.Integer, db.ForeignKey('customer_address.id'))
    #default_shipping = db.relationship("Address", uselist=False, backref="customer")
    shipping_address =db.relationship("Address", foreign_keys=[default_shipping])
    billing_address =db.relationship("Address", foreign_keys=[default_billing], post_update=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Group(db.Model):
    __tablename__ = 'customer_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(254))
    customers = db.relationship('Customer', backref='customer_group', lazy='dynamic')



class Address(db.Model):
    __tablename__ = 'customer_address'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', use_alter=True,name="fk_address_customer"))
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    country_id = db.Column(db.String(32))
    region = db.Column(db.String(64))
    region_id = db.Column(db.String(32))
    postcode = db.Column(db.String(64))
    city = db.Column(db.String(64))
    street = db.Column(db.String(254))
    telephone = db.Column(db.String(64))
    fax = db.Column(db.String(64))
    company = db.Column(db.String(64))
    address_type = db.Column(db.Enum('shipping','billing'))

    external_address_id = db.Column(db.Integer,nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)