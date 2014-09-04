#/usr/bin/env python
#-*- coding:utf8 -*-

from .views import OrderView, CategoryView, ProductView,ShipmentView

urlpatterns = (
    ('/order/', OrderView.as_view('order')),
    ('/category/', CategoryView.as_view('category')),
    ('/product/', ProductView.as_view('product')),
    ('/shipment/', ShipmentView.as_view('shipment')),
)