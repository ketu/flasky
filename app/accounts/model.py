#/usr/bin/env python
#-*- coding:utf8 -*-

from flask.ext.security import UserMixin, RoleMixin
from flask.ext.security.utils import encrypt_password

from app.core import app,db


class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(254), unique=True)
    passwd = db.Column(db.String(128))
    role = db.relationship("Role", backref=db.backref('user', order_by=id))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Role(db.Model,RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(254))


