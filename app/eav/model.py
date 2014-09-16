#/usr/bin/env python
#-*- coding:utf8 -*-

from app.core import db



class Entities(db.Model):
    __tablename__ = 'eav_entity'
    id = db.Column(db.Integer, primary_key=True)
    entity_code = db.Column(db.String(64))
    entity_name = db.Column(db.String(128))
    entity_table = db.Column(db.String(128))


class Attributes(db.Model):
    __tablename__ = 'eav_attribute'
    id = db.Column(db.Integer, primary_key=True)
    entity_type_id = db.Column(db.Integer,db.ForeignKey('eav_entity.id'))
    attribute_code = db.Column(db.String(64))
    backend_type = db.Column(db.String(64),default='static')



