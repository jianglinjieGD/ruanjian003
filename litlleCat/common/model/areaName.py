# coding: utf-8
from sqlalchemy import Column, MetaData, String
from sqlalchemy.schema import FetchedValue
from  application import db_mysql


class AreaName(db_mysql.Model):
    __tablename__ = 'areaName'

    name = Column(String(200), primary_key=True, server_default=FetchedValue(), info='???')
