from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from . import database

class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="author")

class Post(database.Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date_from = Column(Date, default=datetime.date, nullable=False)
    date_to = Column(Date)

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(database.Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    text = Column(String, index=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date_from = Column(Date, default=datetime.date, nullable=False)

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")