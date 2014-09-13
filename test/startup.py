#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import xmlrpclib
import urlparse,urllib2,urllib
import base64


LOCAL_XMLRPC = 'http://127.0.0.1:10000/index.php/api/xmlrpc/'
LOCAL_XMLRPC_USER = 'ketu'
LOCAL_XMLRPC_PASSWD = 'xiaolai123'


REMOTE_XMLRPC = 'http://127.0.0.1:10001/index.php/api/xmlrpc/'
REMOTE_XMLRPC_USER = 'ketu'
REMOTE_XMLRPC_PASSWD = 'xiaolai123'



local_proxy = xmlrpclib.ServerProxy(LOCAL_XMLRPC)
local_session = local_proxy.login(LOCAL_XMLRPC_USER,LOCAL_XMLRPC_PASSWD)


remote_proxy = xmlrpclib.ServerProxy(REMOTE_XMLRPC)
remote_session = remote_proxy.login(REMOTE_XMLRPC_USER,REMOTE_XMLRPC_PASSWD)



ATTRIBUTE_SET_ID =  4



products = local_proxy.call(local_session, 'catalog_product.list',[{'status':1}])



need_upload_count = (len(products))

skus = ['EC'+str(d) for d in range(1200, 1200+need_upload_count*2)]


DEFAULT_CATEGORY_ID = 25
CATEGORIES_MAP = {
    '330': 24,
    '353':23,
    '385':25,
}


for product in products:
    try:

        categories = []
        product = local_proxy.call(local_session, 'catalog_product.info',[product['sku']])
        media = local_proxy.call(local_session,'catalog_product_attribute_media.list',[product['sku']])

        for c in product['categories']:
            if c in CATEGORIES_MAP:
                categories.append(CATEGORIES_MAP[c])


        if not categories:
            categories.append(DEFAULT_CATEGORY_ID)

        stock_data = {
                'qty' : 1000,
                'use_config_manage_stock':1,
                'use_config_min_qty' : 1,
                'use_config_min_sale_qty' :1,
                'use_config_max_sale_qty' :1,
                'use_config_backorders' : 1,
                'use_config_notify_stock_qty': 1,
                'use_config_qty_increments' : 1,
                'use_config_enable_qty_increments' : 1,
                 'is_in_stock' : 1
        }
        upload_data = {
                'categories' : categories,
                'name' : product['name'],
                'chinese':product['sku'],
                'description' : product['specifications'] or "" ,
                'short_description' : product['short_description'] or "",
                'weight' : float(product['weight']) * 1000,
                'status' : 0,
                #'website_ids':[1],
                'visibility' :4,
                'price' : product['price'],
                'tax_class_id' : 0,
                'stock_data' : stock_data
        }

        product_id = remote_proxy.call(remote_session,'product.create',['simple',ATTRIBUTE_SET_ID,skus.pop(0),upload_data])
        print(product_id)
        for m in media:
            try :
                image = urlparse.urljoin('http://www.angelcigs.com','/media/catalog/product'+m['file'])
                content = urllib.urlopen(image)
                type = ['image', 'small_image', 'thumbnail']
                image_data = {
                        'file' : {'content':base64.encodestring(content.read()),'mime' :'image/jpeg'},
                        'types': m['types'],
                        'position' : m['position'],
                        'exclude' : 0
                }
                remote_proxy.call(remote_session,'product_media.create',[product_id,image_data])
            except Exception as e:
                print(e)
                pass
    except Exception as e:
        print(e)
        continue














