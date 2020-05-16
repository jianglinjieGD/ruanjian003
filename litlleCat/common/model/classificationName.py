# coding: utf-8
from sqlalchemy import Column, MetaData, String
from  application import db_mysql


class Classificationname(db_mysql.Model):
    __tablename__ = 'classificationName'

    name = Column(String(20), primary_key=True)
