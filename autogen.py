# coding: utf-8
from sqlalchemy import Column, DateTime, Text, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Post(Base):
    __tablename__ = 'Post'

    id = Column(Text, primary_key=True)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    author = Column(Text, nullable=False)
    avatar = Column(Text)
    title = Column(Text, nullable=False)
    content = Column(Text)
