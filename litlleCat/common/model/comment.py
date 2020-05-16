# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, MetaData, String, Text
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from application import db_mysql


class Comment(db_mysql.Model):
    __tablename__ = 'comment'

    usr_id = Column(ForeignKey('users.usr_id', ondelete='CASCADE'), primary_key=True, nullable=False)
    time = Column(DateTime, primary_key=True, nullable=False, server_default=FetchedValue(), info='????')
    movie_id = Column(ForeignKey('movies.movie_id', ondelete='CASCADE'), nullable=False, index=True)
    content = Column(Text, nullable=False, info='????')

    movie = relationship('Movie', primaryjoin='Comment.movie_id == Movie.movie_id', backref='comments')
    usr = relationship('User', primaryjoin='Comment.usr_id == User.usr_id', backref='comments')

