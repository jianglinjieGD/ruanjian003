# coding: utf-8
from sqlalchemy import Column, MetaData, String
from application import db_mysql





class Testtable(db_mysql.Model):
    __tablename__ = 'testtable'

    name = Column(String(50), primary_key=True)
