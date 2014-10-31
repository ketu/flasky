#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import xmlrpclib
import random

from app.core import db


from app.accounts.model import *



role = Role.objects.get_or_404(name='Administrator')
print(role)
user = User(username = 'ketu.lai',email='ketu.lai@qq.com',password='xiaolai123',role=role)


role.save()
user.save()





user = User.objects.filter(email='ketu.lai@qq.com').first_or_404()
print(user.password_hash)

exit()


