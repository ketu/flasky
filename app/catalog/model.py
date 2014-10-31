#/usr/bin/env python
#-*- coding:utf8 -*-
from mongoengine import signals
from app.core import db

class Category(db.DynamicDocument):
    parent = db.ReferenceField("Category")
    lft = db.IntField()
    rgt = db.IntField()
    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()

    def get_children(self):
        children = Category.query.filter(Category.lft.between(self.lft,self.rgt)).order_by(Category.lft.asc())
        return children

    def get_sub_children(self):
        children = Category.query.filter(Category.lft.between(self.lft,self.rgt)).filter(Category.parent_id.__eq__(self.id)).order_by(Category.lft.asc())
        return children

    def get_sub_children_id(self):
        children = self.get_sub_children()
        children_ids = []
        for child in children:
            children_ids.append(child.id)
        return children_ids


    @staticmethod
    def before_delete_event(sender,document,**kwargs):
        depth = document.rgt - document.lft + 1
        sender.objects.filter(lft__gte=document.lft).filter(rgt__lte=document.rgt).delete()
        sender.objects.filter(lft__gt=document.rgt).update(dec__lft=depth)
        sender.objects.filter(rgt__gt=document.rgt).update(dec__lft=depth)


    @staticmethod
    def before_update_event(sender, document, **kwargs):
        sender.objects.filter(parent = document).order_by("-rgt").update(parent=None)
        sender.objects.filter(lft__gte=document.lft).filter(rgt__lte=document.rgt).update(dec__lft = 1,dec__rgt = 1)
        sender.objects.filter(lft__gt=document.rgt).update(dec__lft = 2)
        sender.objects.filter(rgt__gt=document.rgt).update(dec__rgt = 2)
        Category.before_insert_event(sender,document,**kwargs)

    @staticmethod
    def listen_save_event(sender,document,**kwargs):
        if hasattr(document,"_changed_fields") :
            if "parent" in document._changed_fields:
                Category.before_update_event(sender,document,**kwargs)
        else:
            Category.before_insert_event(sender,document,**kwargs)

    @staticmethod
    def before_insert_event(sender, document, **kwargs):
        parent = document.parent

        lft = 1
        sibling = None
        _filter = None

        if parent :
            sibling = sender.objects.filter(parent = parent).order_by("-rgt").first()
            if sibling is None:
                lft = parent.lft+1
                _filter = parent.lft
        else:
            sibling = sender.objects.order_by("-rgt").first()
            document.parent = None

        if sibling:
            lft = sibling.rgt + 1
            _filter = sibling.rgt

        if _filter :
            sender.objects.filter(lft__gt=_filter).update(inc__lft = 2)
            sender.objects.filter(rgt__gt=_filter).update(inc__rgt =2)

        rgt = lft + 1
        document.lft = lft
        document.rgt = rgt

signals.pre_save.connect(Category.listen_save_event,sender = Category)
signals.pre_delete.connect(Category.before_delete_event,sender=Category)

class Product(db.DynamicDocument):
    sku = db.StringField(required=True,unique=True)
    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()


class ProductGallery(db.DynamicDocument):
    product = db.ReferenceField("Product")
    value = db.StringField(required=True)
