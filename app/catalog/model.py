#/usr/bin/env python
#-*- coding:utf8 -*-
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import aliased,Query
from sqlalchemy.orm.attributes import get_history
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from app.core import db
from app.eav.model import Entity,Attribute


class Category(db.Model):
    __tablename__ = 'catalog_category'
    id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(255))
    parent_id = db.Column(db.Integer,db.ForeignKey('catalog_category.id'),nullable=True)
    parent = db.relationship("Category",remote_side =[id],uselist=False)
    entity_type_id = db.Column(db.Integer,db.ForeignKey('eav_entity.id'))
    lft = db.Column(db.Integer, nullable=True)
    rgt = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,onupdate=datetime.utcnow)


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

    def get_product(self):

        children_ids = self.get_sub_children_id()
        children_ids.insert(0,self.id)


        product = Product.query.filter(Product.categories.any(Category.id.in_(children_ids)))

        attributes = Product.get_list_attributes()


        for attr in attributes:
            backend_type = catalog_product_entity_table_map[attr.backend_type]
            if not backend_type:
                continue
            product = product.outerjoin(backend_type,backend_type.entity_id == Product.id).add_column(backend_type.value)

        print(product)
        return product.all()






    @staticmethod
    def before_delete_event(mapper,connection,target):
        depth = target.rgt - target.lft + 1
        mapper.confirm_deleted_rows = False
        Category.query.filter(Category.lft.between(target.lft,target.rgt)).delete(synchronize_session=False)
        Category.query.filter(Category.lft.__gt__(target.rgt)).update(dict(lft=Category.lft - depth))
        Category.query.filter(Category.rgt.__gt__(target.rgt)).update(dict(rgt=Category.rgt - depth))

    @staticmethod
    def before_update_event(mapper,connection,target):
        original_target_parent_data =  get_history(target,'parent_id')
        unchanged_parent_id = original_target_parent_data[1]
        if not unchanged_parent_id :
            Category.query.filter(Category.lft.between(target.lft,target.rgt)).update(dict(lft=Category.lft - 1,rgt=Category.rgt-1),synchronize_session=False)
            Category.query.filter(Category.lft.__gt__(target.rgt)).update(dict(lft=Category.lft - 2),synchronize_session=False)
            Category.query.filter(Category.lft.__gt__(target.rgt)).update(dict(lft=Category.lft - 2),synchronize_session=False)
            Category.before_insert_event(mapper,connection,target)


    @staticmethod
    def before_insert_event(mapper, connection, target):
        parent_id = target.parent_id
        lft = 1
        sibling = None
        _filter = None
        parent = None
        if parent_id :
            parent = Category.query.filter(Category.id.__eq__(parent_id)).first()
            if parent :
                sibling = Category.query.filter(Category.parent_id.__eq__(parent_id)).order_by(Category.rgt.desc()).first()
                if sibling is None:
                    lft = parent.lft+1
                    _filter = parent.lft

        if parent is None:
            sibling = Category.query.order_by(Category.rgt.desc()).first()
            target.parent_id = None

        if sibling:
            lft = sibling.rgt + 1
            _filter = sibling.rgt

        if _filter :
            Category.query.filter(Category.lft.__gt__(_filter)).update(dict(lft=Category.lft +2))
            Category.query.filter(Category.rgt.__gt__(_filter)).update(dict(rgt=Category.rgt +2))

        rgt = lft + 1
        target.lft = lft
        target.rgt = rgt


db.event.listen(Category, 'before_delete', Category.before_delete_event, propagate =True,retval=True)
db.event.listen(Category, 'before_update', Category.before_update_event, propagate =True,retval=True)
db.event.listen(Category, 'before_insert', Category.before_insert_event, propagate =True,retval=True)





category_product = db.Table('catalog_category_product',
    db.Column('category_id', db.Integer, db.ForeignKey('catalog_category.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('catalog_product.id'))
)

class Product(db.Model):
    __tablename__ = 'catalog_product'
    id = db.Column(db.Integer, primary_key=True)
    entity_type_id = db.Column(db.Integer,db.ForeignKey('eav_entity.id'))
    sku = db.Column(db.String(64),unique=True)

    categories = db.relationship('Category', secondary=category_product,lazy='dynamic')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


    @hybrid_property
    def data(self):
        return self.data

    @data.setter
    def data(self,data):
        self.data=data


    @staticmethod
    def get_entity_type():
        entity = Entity.query.filter_by(entity_code='catalog_product').one()
        return entity

    @staticmethod
    def get_list_attributes():
        attributes = Product.get_attributes()
        return attributes

    @staticmethod
    def get_attributes():
        entity = Product.get_entity_type()
        attributes = Attribute.query.filter_by(entity_type_id= entity.id).all()
        return attributes


class ProductGallery(db.Model):
    __tablename__ = 'catalog_product_gallery'
    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer,db.ForeignKey('catalog_product.id'))
    value = db.Column(db.String(255))



class ProductEntityVarchar(db.Model):
    __tablename__ = 'catalog_product_entity_varchar'
    id = db.Column(db.Integer, primary_key=True)
    entity_type_id = db.Column(db.Integer,db.ForeignKey('eav_entity.id'))
    attribute_id = db.Column(db.Integer,db.ForeignKey('eav_attribute.id'))
    store_id = db.Column(db.Integer, default=0)
    entity_id = db.Column(db.Integer,db.ForeignKey('catalog_product.id'))
    value = db.Column(db.String(255),nullable=True,default=None)


class ProductEntityDecimal(db.Model):
    __tablename__ = 'catalog_product_entity_decimal'
    id = db.Column(db.Integer, primary_key=True)
    entity_type_id = db.Column(db.Integer,db.ForeignKey('eav_entity.id'))
    attribute_id = db.Column(db.Integer,db.ForeignKey('eav_attribute.id'))
    store_id = db.Column(db.Integer, default=0)
    entity_id = db.Column(db.Integer,db.ForeignKey('catalog_product.id'))
    value = db.Column(db.Numeric(12,4),nullable=True,default=None)


class ProductEntityInt(db.Model):
    __tablename__ = 'catalog_product_entity_int'
    id = db.Column(db.Integer, primary_key=True)
    entity_type_id = db.Column(db.Integer,db.ForeignKey('eav_entity.id'))
    attribute_id = db.Column(db.Integer,db.ForeignKey('eav_attribute.id'))
    store_id = db.Column(db.Integer, default=0)
    entity_id = db.Column(db.Integer,db.ForeignKey('catalog_product.id'))
    value = db.Column(db.Integer,nullable=True,default=None)

class ProductEntityText(db.Model):
    __tablename__ = 'catalog_product_entity_text'
    id = db.Column(db.Integer, primary_key=True)
    entity_type_id = db.Column(db.Integer,db.ForeignKey('eav_entity.id'))
    attribute_id = db.Column(db.Integer,db.ForeignKey('eav_attribute.id'))
    store_id = db.Column(db.Integer, default=0)
    entity_id = db.Column(db.Integer,db.ForeignKey('catalog_product.id'))
    value = db.Column(db.Text,nullable=True,default=None)



catalog_product_entity_table_map = {
    'varchar':ProductEntityVarchar,
    'decimal':ProductEntityDecimal,
    'int':ProductEntityInt,
    'text':ProductEntityText,
}