#/usr/bin/env python
#-*- coding:utf8 -*-
from datetime import datetime

from app.core import db
from app.dashboard.model import Website


class Order(db.Document):
    increment_id = db.StringField(required=True,unique=True)
    website = db.ReferenceField("Website")

    state = db.StringField(required=True)
    coupon_code = db.StringField()

    shipping_description = db.StringField(required=True)
    shipping_method = db.StringField(required=True)


    customer = db.ReferenceField("Customer")
    customer_note = db.StringField()

    grand_total = db.DecimalField(required=True)
    base_grand_total = db.DecimalField(required=True)
    shipping_amount = db.DecimalField(default=0.0000)
    base_shipping_amount = db.DecimalField(default=0.0000)
    discount_amount = db.DecimalField(default=0.0000)
    base_discount_amount = db.DecimalField(default=0.0000)
    subtotal = db.DecimalField(required=True)
    base_subtotal = db.DecimalField(required=True)
    base_currency_code = db.StringField(required=True)
    currency_code = db.StringField(required=True)

    shipping_address = db.ReferenceField("Address")
    billing_address = db.ReferenceField("Address")

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()

class OrderItem(db.Document):

    order = db.ReferenceField("Order")
    product = db.ReferenceField("Product")

    product_options = db.StringField()
    name = db.StringField(required=True)
    sku = db.StringField(required=True)
    qty_ordered = db.IntField(required=True)
    original_price = db.DecimalField()
    base_original_price	 = db.DecimalField()
    price = db.DecimalField()
    base_price = db.DecimalField()
    weight = db.DecimalField()
    row_weight = db.DecimalField()
    base_row_total = db.DecimalField()
    row_total = db.DecimalField()
    created_at = db.DateTimeField()


class Invoice(db.Document):
    order = db.ReferenceField("Order")
    email_sent = db.BooleanField()
    created_at = db.DateTimeField()

class Payment(db.Document):
    order = db.ReferenceField("Order")
    shipping_captured = db.DecimalField()
    base_shipping_captured =db.DecimalField()
    base_amount_ordered = db.DecimalField()
    amount_ordered =db.DecimalField()
    base_amount_paid = db.DecimalField()
    amount_paid = db.DecimalField()
    base_shipping_amount = db.DecimalField()
    shipping_amount = db.DecimalField()
    payment_method = db.StringField(required=True)
    last_trans_id = db.StringField()
    additional_data = db.StringField()


class Shipment(db.Document):
    order = db.ReferenceField("Order")
    tracking = db.ReferenceField("ShipmentTrack")
    total_weight = db.DecimalField()
    total_qty = db.DecimalField()
    email_sent = db.BooleanField()
    created_at = db.DateTimeField()

class ShipmentTrack(db.Document):
    shipment = db.ReferenceField("Shipment")
    title = db.StringField(required=True)
    track_number = db.StringField(required=True)
    carrier_code = db.StringField(required=True)
    description = db.StringField()
    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()


class ShipmentItem(db.Document):
    shipment = db.ReferenceField("Shipment")
    product_id = db.ReferenceField("Product")
    order_item_id = db.ReferenceField("OrderItem")
    name = db.StringField()
    sku = db.StringField()
    qty = db.IntField()
    weight = db.DecimalField()
    additional_data = db.StringField()







