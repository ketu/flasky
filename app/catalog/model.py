#/usr/bin/env python
#-*- coding:utf8 -*-
from datetime import datetime

from app.core import db
from app.dashboard.model import Website


class Category(db.Model):
    __tablename__ = 'catalog_category'
    id = db.Column(db.Integer, primary_key=True)

class Product(db.Model):
    __tablename__ = 'catalog_product'
    id = db.Column(db.Integer, primary_key=True)


class Attribute(db.Model):
    __tablename__ = 'eav_attribute'
    id = db.Column(db.Integer, primary_key=True)
