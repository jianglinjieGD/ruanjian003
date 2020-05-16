# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, MetaData, String, Text
from sqlalchemy.schema import FetchedValue
from application import db_mysql


class Movie(db_mysql.Model):
    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, index=True, server_default=FetchedValue(), info='????')
    other_name = Column(String(200), nullable=False, index=True, server_default=FetchedValue(), info='????')
    classification = Column(String(100), nullable=False, index=True, server_default=FetchedValue(), info='??')
    director = Column(String(500), nullable=False, index=True, server_default=FetchedValue(), info='??')
    actors = Column(String(500), nullable=False, index=True, server_default=FetchedValue(), info='??')
    cover_pic = Column(String(300), nullable=False, server_default=FetchedValue(), info='???')
    pics = Column(String(1000), nullable=False, server_default=FetchedValue(), info='??????json? ?? ??')
    description = Column(Text, nullable=False, info='????')
    imdb_url = Column(String(5000), nullable=False, server_default=FetchedValue(), info='IMDb_url??????')
    vid_url = Column(String(5000), nullable=False, server_default=FetchedValue(), info='???????????')
    hash = Column(String(32), nullable=False, unique=True, server_default=FetchedValue(), info='hash???')
    pub_date = Column(DateTime, nullable=False, index=True, server_default=FetchedValue(), info='????')
    source = Column(String(20), nullable=False, server_default=FetchedValue(), info='?????, douban')
    view_count = Column(Integer, nullable=False, server_default=FetchedValue(), info='???')
    update_time = Column(DateTime, nullable=False, server_default=FetchedValue(), info='??????')
    create_time = Column(DateTime, nullable=False, server_default=FetchedValue(), info='????')
    douban_score = Column(Integer, nullable=False, index=True, server_default=FetchedValue(), info='????')
    love_count = Column(Integer, nullable=False, server_default=FetchedValue(), info='???')
    comment_count = Column(Integer, nullable=False, server_default=FetchedValue(), info='???')
    info_url = Column(String(300), nullable=False, server_default=FetchedValue(), info='????????')
    area = Column(String(100), nullable=False, index=True, server_default=FetchedValue(), info='??')
