#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
import xmlrpclib
import random
import re
import requests
import base64
import glob





attribute_set = 13
category_id = 5

LOCAL_XMLRPC = 'http://www.beautifultech.com/index.php/api/xmlrpc/'
#LOCAL_XMLRPC = 'http://127.0.0.1:8089/index.php/api/xmlrpc/'
LOCAL_XMLRPC_USER = 'ketu'
LOCAL_XMLRPC_PASSWD = 'xiaolai123'

local_proxy = xmlrpclib.ServerProxy(LOCAL_XMLRPC)
local_session = local_proxy.login(LOCAL_XMLRPC_USER,LOCAL_XMLRPC_PASSWD)


REMOTE_XMLRPC = 'http://www.mydealszone.com/index.php/api/xmlrpc/'
#REMOTE_XMLRPC = 'http://127.0.0.1:8089/index.php/api/xmlrpc/'
REMOTE_XMLRPC_USER = 'ketu'
REMOTE_XMLRPC_PASSWD = 'xiaolai123'

remote_proxy = xmlrpclib.ServerProxy(REMOTE_XMLRPC,allow_none=True)
remote_session = remote_proxy.login(REMOTE_XMLRPC_USER,REMOTE_XMLRPC_PASSWD)





products = local_proxy.call(local_session,'catalog_product.list',[{'attribute_set_id':14}])

download_image_path = "images/"
for p in products:
    try:

        tmp_download_image_path = download_image_path + p['sku']

        if not os.path.isdir(tmp_download_image_path):
            os.mkdir(tmp_download_image_path)

        images = local_proxy.call(local_session,'product_attribute_media.list',[p['sku']])



        for i in images:



            file_name =os.path.basename(i['file']).lower()

            _path = os.path.join(tmp_download_image_path,file_name)


            r = requests.get(i['url'], stream=True,timeout=60)
            if r.status_code == 200:

                with open(_path, 'wb') as f:
                    for chunk in r.iter_content():
                        f.write(chunk)

        p = local_proxy.call(local_session,'catalog_product.info',[p['sku']])
        #print(p)

        sku ="SKU" + p['sku'].replace((re.sub("\d+",'',p['sku'])),"")

        stock_data = {
                        'qty' : 1000,
                        'use_config_manage_stock':1,
                        'use_config_min_qty' : 1,
                        'use_config_min_sale_qty' :1,
                        'use_config_max_sale_qty' :1,
                        #'is_qty_decimal' : 1,
                        'use_config_backorders' : 1,
                        'use_config_notify_stock_qty': 1,
                        'use_config_qty_increments' : 1,
                        'use_config_enable_qty_increments' : 1,
                        'is_in_stock' : 1
                    }

        upload_data = {
                        'categories' : [category_id],
                        'name' : p['name'],
                        'chinese':p['chinese'],
                        'purchase_link':p['purchase_link'],
                        'description' : p['description'],
                        'short_description' : p['short_description'],
                        'weight' : p['weight'],
                        'status' : 1,
                        'visibility' :4,
                        'price' : p['price'],
                        'cost' :p['cost'],
                        'tax_class_id' : 0,
                        'stock_data' : stock_data
        }
        product_id = remote_proxy.call(remote_session,'product.create',['simple',attribute_set,sku,upload_data])

        images = glob.glob('images/%s/*.jpg'%p['sku'])
        if images:
            i = 1
            for image in images:
                try:
                    _type = []
                    if i == 1:
                        _type = ['image', 'small_image', 'thumbnail']
                    with open(image,'rb') as fp:
                        content = fp.read()
                        image_data = {
                                        'file' : {'content':base64.encodestring(content),'mime' :'image/jpeg'},
                                        'types': _type,
                                        'position' : i,
                                        'exclude' : 0
                                    }
                        remote_proxy.call(remote_session,'product_media.create',[product_id,image_data])
                        i += 1
                except Exception as e:
                        print(e)
                        print(image)
                        pass


    except Exception as e:
        print(e)
        continue



