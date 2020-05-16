# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, MetaData, String, Text
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from application import db_mysql


class Carousel(db_mysql.Model):
    __tablename__ = 'carousel'

    carousel_id = Column(Integer, primary_key=True, info='???id')
    movie_id = Column(ForeignKey('movies.movie_id', ondelete='CASCADE'), nullable=False, index=True, info='??id')
    name = Column(String(200), nullable=False, server_default=FetchedValue(), info='????')
    huge_pic = Column(String(300), nullable=False, server_default=FetchedValue(), info='???')

    movie = relationship('Movie', primaryjoin='Carousel.movie_id == Movie.movie_id', backref='carousels')

