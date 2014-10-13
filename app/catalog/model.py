#/usr/bin/env python
#-*- coding:utf8 -*-
from datetime import datetime
from flask.ext import sqlalchemy
from sqlalchemy.orm.attributes import get_history

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
    def before_delete_event(mapper,connection,target):
        print('asdfsdafda')
        connection.dispatch = None
        connection._has_events = False
        connection.engine._has_events = False
        print(connection)
        depth = target.rgt - target.lft + 1
        #trans = connection.begin()

        #connection.execute("UPDATE "+Category.__tablename__+" SET `lft`=`lft`-1,`rgt`=`rgt`-1 WHERE `lft` BETWEEN %s AND %s",target.lft,target.rgt)

        connection.execute("DELETE FROM "+Category.__tablename__+" WHERE `lft` BETWEEN %s AND %s",target.lft,target.rgt)
        connection.execute("UPDATE "+Category.__tablename__+" SET `lft`=`lft`-%s WHERE lft > %s",depth,target.rgt)
        connection.execute("UPDATE "+Category.__tablename__+" SET `rgt`=`rgt`-%s WHERE rgt > %s",depth,target.rgt)
        #connection.execute("UPDATE "+Category.__tablename__+" SET `parent_id` = %s WHERE `parent_id` = %s",target.parent_id,target.id,execution_options={})
        #trans.commit()



    @staticmethod
    def before_update_event(mapper,connection,target):
        original_target_parent_data =  get_history(target,'parent_id')
        print(123423)
        unchanged_parent_id = original_target_parent_data[1]
        if not unchanged_parent_id :
            #Category.query.filter(Category.lft.between(target.lft,target.rgt)).update(
            #    dict(lft=Category.lft -1,rgt = Category.rgt -1))


            connection.execute("UPDATE "+Category.__tablename__+" SET `lft`=`lft`-1,`rgt`=`rgt`-1 WHERE `lft` BETWEEN %s AND %s",target.lft,target.rgt)
            connection.execute("UPDATE "+Category.__tablename__+" SET `lft`=`lft`-2 WHERE lft > %s",target.rgt)
            connection.execute("UPDATE "+Category.__tablename__+" SET `rgt`=`rgt`-2 WHERE rgt > %s",target.rgt)

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

class Product(db.Model):
    __tablename__ = 'catalog_product'
    id = db.Column(db.Integer, primary_key=True)
    entity_type_id = db.Column(db.Integer,db.ForeignKey('eav_entity.id'))
    sku = db.Column(db.String(64),unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)