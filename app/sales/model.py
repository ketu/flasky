#/usr/bin/env python
#-*- coding:utf8 -*-
from datetime import datetime

from app.core import db
from app.dashboard.model import Website


class Order(db.Model):
    __tablename__ = 'sales_order'
    id = db.Column(db.Integer, primary_key=True)
    increment_id = db.Column(db.String(128),unique=True)
    website_id = db.Column(db.Integer, db.ForeignKey('website.id'))
    website = db.relationship("Website", uselist=False, backref="sales_order")
    state = db.Column(db.String(32))
    coupon_code = db.Column(db.String(32),nullable=True)

    shipping_description = db.Column(db.String(128))
    shipping_method = db.Column(db.String(128))

    customer_id	= db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship("Customer", uselist=False, backref="sales_order")
    customer_note = db.Column(db.Text,nullable=True)

    grand_total = db.Column(db.Numeric(12,4))
    base_grand_total = db.Column(db.Numeric(12,4))
    shipping_amount = db.Column(db.Numeric(12,4),default=0.0000)
    base_shipping_amount = db.Column(db.Numeric(12,4),default=0.0000)
    discount_amount = db.Column(db.Numeric(12,4),default=0.0000)
    base_discount_amount = db.Column(db.Numeric(12,4),default=0.0000)
    subtotal = db.Column(db.Numeric(12,4))
    base_subtotal = db.Column(db.Numeric(12,4))
    base_currency_code = db.Column(db.String(12))
    currency_code = db.Column(db.String(12))

    shipping_address_id = db.Column(db.Integer, db.ForeignKey('customer_address.id'))
    billing_address_id = db.Column(db.Integer, db.ForeignKey('customer_address.id'))

    shipping_address =db.relationship("Address", foreign_keys=[shipping_address_id])
    billing_address =db.relationship("Address", foreign_keys=[billing_address_id], post_update=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class OrderItem(db.Model):
    __tablename__ = 'sales_order_item'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('sales_order.id'))
    order = db.relationship("Order", uselist=False, backref="sales_order_item")
    product_id = db.Column(db.Integer, db.ForeignKey('catalog_product.id'))
    product_options = db.Column(db.Text)
    name = db.Column(db.String(255))
    sku = db.Column(db.String(128))
    qty_ordered = db.Column(db.Numeric(12,4))
    original_price = db.Column(db.Numeric(12,4))
    base_original_price	 = db.Column(db.Numeric(12,4))
    price = db.Column(db.Numeric(12,4))
    base_price = db.Column(db.Numeric(12,4))
    weight = db.Column(db.Numeric(12,4))
    row_weight = db.Column(db.Numeric(12,4))
    base_row_total = db.Column(db.Numeric(12,4))
    row_total = db.Column(db.Numeric(12,4))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Invoice(db.Model):
    __tablename__ = 'sales_invoice'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('sales_order.id'))
    order = db.relationship("Order", uselist=False, backref="sales_invoice")

    email_sent = db.Column(db.Boolean,default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    __tablename__ = 'sales_payment'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('sales_order.id'))
    order = db.relationship("Order", uselist=False, backref="sales_payment")
    shipping_captured = db.Column(db.Numeric(12,4))
    base_shipping_captured = db.Column(db.Numeric(12,4))
    base_amount_ordered = db.Column(db.Numeric(12,4))
    amount_ordered = db.Column(db.Numeric(12,4))
    base_amount_paid = db.Column(db.Numeric(12,4))
    amount_paid = db.Column(db.Numeric(12,4))
    base_shipping_amount = db.Column(db.Numeric(12,4))
    shipping_amount = db.Column(db.Numeric(12,4))
    payment_method = db.Column(db.String(128))
    last_trans_id = db.Column(db.String(255),nullable=True)
    additional_data = db.Column(db.Text,nullable=True)


class Shipment(db.Model):
    __tablename__ = 'sales_shipment'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('sales_order.id'))
    order = db.relationship("Order", uselist=False, backref="sales_shipment")
    tracking = db.relationship("ShipmentTrack", backref="sales_shipment")
    total_weight = db.Column(db.Numeric(12,4),nullable=True)
    total_qty = db.Column(db.Numeric(12,4),nullable=True)
    email_sent = db.Column(db.Boolean,default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class ShipmentTrack(db.Model):
    __tablename__ = 'sales_shipment_track'
    id = db.Column(db.Integer, primary_key=True)
    shipment_id = db.Column(db.Integer, db.ForeignKey('sales_shipment.id'))
    title = db.Column(db.String(128))
    track_number = db.Column(db.String(128))
    carrier_code = db.Column(db.String(128))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class ShipmentItem(db.Model):
    __tablename__ = 'sales_shipment_item'
    id = db.Column(db.Integer, primary_key=True)
    shipment_id = db.Column(db.Integer, db.ForeignKey('sales_shipment.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('catalog_product.id'))
    order_item_id = db.Column(db.Integer, db.ForeignKey('sales_order_item.id'))
    name = db.Column(db.String(255))
    sku = db.Column(db.String(128))
    qty = db.Column(db.Numeric(12,4))
    weight = db.Column(db.Numeric(12,4))
    additional_data = db.Column(db.Text)







