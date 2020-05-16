# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db_mysql


class User(db_mysql.Model):
    __tablename__ = 'users'

    usr_id = Column(Integer, primary_key=True, info='??')
    nickname = Column(String(30), nullable=False, server_default=FetchedValue(), info='??')
    login_name = Column(String(20), nullable=False, unique=True, server_default=FetchedValue(), info='?????')
    login_pwd = Column(String(32), nullable=False, server_default=FetchedValue(), info='??????')
    login_salt = Column(String(32), nullable=False, server_default=FetchedValue(), info='?????????')
    status = Column(Integer, nullable=False, server_default=FetchedValue(), info='?? 0??? 1???')
    updated_time = Column(DateTime, nullable=False, server_default=FetchedValue(), info='????????')
    created_time = Column(DateTime, nullable=False, server_default=FetchedValue(), info='????')
    head_pic = Column(String(300), nullable=False, server_default=FetchedValue(), info='??')
