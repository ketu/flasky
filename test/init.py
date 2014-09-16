#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import xmlrpclib
import urlparse,urllib2,urllib
import base64
from app.core import db
from app.catalog.model import Category,Product

LOCAL_XMLRPC = 'http://127.0.0.1:10000/index.php/api/xmlrpc/'
LOCAL_XMLRPC_USER = 'ketu'
LOCAL_XMLRPC_PASSWD = 'xiaolai123'




local_proxy = xmlrpclib.ServerProxy(LOCAL_XMLRPC)
local_session = local_proxy.login(LOCAL_XMLRPC_USER,LOCAL_XMLRPC_PASSWD)







products = local_proxy.call(local_session, 'catalog_product.list',[{'status':1}])




for product in products:
    try:
        p = Product(sku = product['sku'],entity_type_id =2)
        db.session.add(p)
    except Exception as e:
        print(e)
        continue



db.session.commit()












