import os
import xmlrpclib

from .abstract import Abstract


class Magento(Abstract):

    def __init__(self):
        pass

    def get_order_list(self):
        pass

    def get_order(self):
        pass

    def update_order(self):
        pass

    def create_invoice(self):
        pass

    def update_invoice(self):
        pass

    def get_category(self):
        pass

    def get_category_list(self):
        pass

    def get_product_list(self):
        pass

    def get_product(self,sku):
        pass

    def update_product(self,sku):
        pass

    def create_shipment(self):
        pass

    def update_shipment(self):
        pass

    def add_track_number(self):
        pass

