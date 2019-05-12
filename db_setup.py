import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    image_file = Column(String(20), nullable=False, default='default.jpg')
    password = Column(String(60), nullable=False)
    #posts = relationship ('Post', backref='author', lazy=True)


"""
class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

"""


class Tournaments(Base):
    __tablename__ = 'tournament'

    id = Column(Integer, primary_key=True)
    tournamentName = Column(String(180), nullable=False)
    gameSystem = Column(String(100), nullable=False)
    postCode = Column(String(5), nullable=False)
    city = Column(String(100), nullable=False)
    startDate = Column(String(100), nullable=False)
    lat = Column(Integer, nullable=True)
    longg = Column(Integer, nullable=True)


engine = create_engine('sqlite:///tournament.db?check_same_thread=False')


Base.metadata.create_all(engine)




