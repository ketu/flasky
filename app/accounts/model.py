#/usr/bin/env python
#-*- coding:utf8 -*-
from flask import current_app
from flask.ext.security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.core import db



class User(db.DynamicDocument,UserMixin):
    username = db.StringField(required=True,unique=True)
    email = db.EmailField(required=True,unique=True)
    password_hash = db.StringField(required=True)
    role = db.ReferenceField("Role")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})


class Role(db.Document,RoleMixin):
    name = db.StringField(required =True,unique=True)



