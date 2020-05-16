# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, MetaData, String, Text
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship

from application import db_mysql


class History(db_mysql.Model):
    __tablename__ = 'history'

    usr_id = Column(ForeignKey('users.usr_id', ondelete='CASCADE'), primary_key=True, nullable=False)
    movie_id = Column(ForeignKey('movies.movie_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
    love = Column(Integer, nullable=False, server_default=FetchedValue(), info='??????')
    isHistory = Column(Integer, nullable=False, server_default=FetchedValue(), info='??????')

    movie = relationship('Movie', primaryjoin='History.movie_id == Movie.movie_id', backref='histories')
    usr = relationship('User', primaryjoin='History.usr_id == User.usr_id', backref='histories')

