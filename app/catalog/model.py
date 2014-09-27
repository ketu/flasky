#/usr/bin/env python
#-*- coding:utf8 -*-
from datetime import datetime

from flask.ext import sqlalchemy
from app.core import db
from app.eav.model import Entities


class Category(db.Model):
    __tablename__ = 'catalog_category'
    id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(255))
    parent_id = db.Column(db.Integer,db.ForeignKey('catalog_category.id'),nullable=True)
    parent = db.relationship("Category", uselist=False, foreign_keys=[parent_id])
    entity_type_id = db.Column(db.Integer,db.ForeignKey('eav_entity.id'))
    lft = db.Column(db.Integer, nullable=True)
    rgt = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,onupdate=datetime.utcnow)



    @staticmethod
    def before_insert_or_update_event(mapper, connection, target):
        parent_id = target.parent_id
        parent = None
        lft = 1
        gt_filter = None

        if parent_id :
            parent = Category.query.get(parent_id)

        if parent:
            gt_filter = parent.lft
            lft = parent.lft + 1
        else:
            parent = Category.query.order_by(Category.rgt.desc()).first()

            #print(parent.id)
            if parent is not None:
                #gt_filter = parent.rgt
                lft = parent.rgt + 1


        if gt_filter :
            Category.query.filter(Category.lft.__gt__(gt_filter)).update(dict(lft=Category.lft +2))
            Category.query.filter(Category.rgt.__gt__(gt_filter)).update(dict(rgt=Category.rgt +2))

            #Category.objects().filter_by(rgt__gt = gtFilter).update(rgt = models.F('rgt') + 2)


        rgt = lft + 1
        target.lft = lft
        target.rgt = rgt

    @staticmethod
    def before_delete(mapper, connection, target):

        print('asfdsf')
        print(mapper)
        print(connection)


        return sqlalchemy.orm.interfaces.EXT_STOP

#db.event.listen(Category, 'before_delete', Category.before_delete, propagate =True,retval=True)
db.event.listen(Category, 'before_update', Category.before_insert_or_update_event, propagate =True,retval=True)
db.event.listen(Category, 'before_insert', Category.before_insert_or_update_event, propagate =True,retval=True)

class Product(db.Model):
    __tablename__ = 'catalog_product'
    id = db.Column(db.Integer, primary_key=True)
    entity_type_id = db.Column(db.Integer,db.ForeignKey('eav_entity.id'))
    sku = db.Column(db.String(64),unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)