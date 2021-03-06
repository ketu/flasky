#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import xmlrpclib
import random

from app.core import db

from app.customers.model import Customer,Address
from app.catalog.model import Category,Product
from app.sales.model import Order,Shipment,Invoice,OrderItem
from mongoengine.fields import ObjectId



LOCAL_XMLRPC = 'http://127.0.0.1:8089/index.php/api/xmlrpc/'
LOCAL_XMLRPC_USER = 'ketu'
LOCAL_XMLRPC_PASSWD = 'xiaolai123'




local_proxy = xmlrpclib.ServerProxy(LOCAL_XMLRPC)
local_session = local_proxy.login(LOCAL_XMLRPC_USER,LOCAL_XMLRPC_PASSWD)


parent_ids = []
test = Category.objects().all()
for t in test:
    print(t.name,t.id,t.lft,t.rgt)
    parent_ids.append(t.id)

#print(parent_ids)

object_id = ObjectId(random.sample(parent_ids,1)[0])

parent_category = Category.objects.get(id='544f559e3d49242a698eca5e')

print(object_id)
load_category = Category.objects.get(name = 'Cables')
print(load_category.name)
load_category.parent = parent_category

load_category.save()
test = Category.objects().all()
for t in test:
    print(t.name,t.id,t.lft,t.rgt)
exit()

categories = local_proxy.call(local_session,'catalog_category.tree',[3])


for category in categories['children']:
    #print(category)

    c = Category(
        #parent_id = random.sample(range(1,9),1)

        name = category['name']


    )

    c.save()
    #exit()



exit()





orders = local_proxy.call(local_session, 'order.list')

for order in orders:
    order = local_proxy.call(local_session, 'order.info',[order['increment_id']])







    customer = Customer.query.filter_by(email = order['customer_email']).first()
    if customer is None:
        customer = Customer(email = order['customer_email'],website_id = 1,firstname=order['customer_firstname'],lastname=order['customer_lastname'] )
        db.session.add(customer)



    shipping_address = Address.query.filter_by(external_address_id = order['shipping_address_id']).first()
    if shipping_address is None:
        order_shipping_address = order['shipping_address']
        shipping_address = Address(customer_id = customer.id,
                                   firstname = order_shipping_address['firstname'],
                                   lastname = order_shipping_address['lastname'],
                                   country_id = order_shipping_address['country_id'],
                                   region = order_shipping_address['region'],
                                   postcode = order_shipping_address['postcode'],
                                   city = order_shipping_address['city'],
                                   street = order_shipping_address['street'],
                                   telephone = order_shipping_address['telephone'],
                                   fax = order_shipping_address['fax'],
                                   company = order_shipping_address['company'],
                                   address_type = order_shipping_address['address_type']
                                   )
        db.session.add(shipping_address)

    billing_address = Address.query.filter_by(external_address_id = order['billing_address_id']).first()
    if billing_address is None:
        order_billing_address = order['billing_address']
        billing_address = Address(customer_id = customer.id,
                                   firstname = order_billing_address['firstname'],
                                   lastname = order_billing_address['lastname'],
                                   country_id = order_billing_address['country_id'],
                                   region = order_billing_address['region'],
                                   postcode = order_billing_address['postcode'],
                                   city = order_billing_address['city'],
                                   street = order_billing_address['street'],
                                   telephone = order_billing_address['telephone'],
                                   fax = order_billing_address['fax'],
                                   company = order_billing_address['company'],
                                   address_type = order_billing_address['address_type']
                                   )
        db.session.add(billing_address)




    _order = Order(increment_id = order['increment_id'],website_id=1,state = order['state'],shipping_method=order['shipping_method'],
            shipping_description = order['shipping_description'],
            customer_id = customer.id,
            grand_total = order['grand_total'],
            base_grand_total = order['base_grand_total'],
            shipping_amount = order['shipping_amount'],
            base_shipping_amount = order['base_shipping_amount'],
            discount_amount = order['discount_amount'],
            base_discount_amount = order['base_discount_amount'],
            subtotal = order['subtotal'],
            base_subtotal = order['base_subtotal'],
            base_currency_code = order['base_currency_code'],
            currency_code = order['order_currency_code'],
            shipping_address_id = shipping_address.id,
            billing_address_id = billing_address.id
              )
    db.session.add(_order)


    #print(_order.id)
    for item in order['items']:


        product = Product.query.filter_by(sku = item['sku']).first()
        if product is None:
            product = Product(sku = item['sku'])
            db.session.add(product)


        order_item = OrderItem(order_id = _order.id,product_id= product.id,product_options=item['product_options'],
                               name = item['name'],
                               sku = item['sku'],
                               qty_ordered = item['qty_ordered'],
                               original_price = item['original_price'],
                               base_original_price = item['base_original_price'],
                               price = item['price'],
                               base_price = item['base_price'],
                               row_weight = item['row_weight'],
                               weight = item['weight'],
                               base_row_total = item['base_row_total'],
                               row_total = item['row_total']
                               )
        db.session.add(order_item)




db.session.commit()












