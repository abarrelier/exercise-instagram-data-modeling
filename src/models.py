import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    posts = relationship('Post', back_populates='user') # back indica el lado inverso de una relación bidireccional entre dos modelos.
    followers = relationship('Follow', foreign_keys='Follow.following_id', back_populates='following')#indicar clave foranea
    following = relationship('Follow', foreign_keys='Follow.follower_id', back_populates='follower')
    likes = relationship('Like', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    messages_sent = relationship('Message', foreign_keys='Message.sender_id', back_populates='sender')
    messages_received = relationship('Message', foreign_keys='Message.receiver_id', back_populates='receiver')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    image_url = Column(String(200), nullable=False)
    caption = Column(String(200))
    created_at = Column(DateTime, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='posts')
    likes = relationship('Like', back_populates='post')
    comments = relationship('Comment', back_populates='post')

class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    user = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='likes')

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    text = Column(String(200), nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

class Follow(Base):
    __tablename__ = 'follow'
    id = Column(Integer, primary_key=True)

    follower_id = Column(Integer, ForeignKey('user.id'))
    following_id = Column(Integer, ForeignKey('user.id'))
    follower = relationship('User', foreign_keys=[follower_id], back_populates='following')
    following = relationship('User', foreign_keys=[following_id], back_populates='followers')

class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    text = Column(String(200), nullable=False)
    sent_at = Column(DateTime, nullable=False)

    sender_id = Column(Integer, ForeignKey('user.id'))
    receiver_id = Column(Integer, ForeignKey('user.id'))
    sender = relationship('User', foreign_keys=[sender_id], back_populates='messages_sent')
    receiver = relationship('User', foreign_keys=[receiver_id], back_populates='messages_received')




    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
