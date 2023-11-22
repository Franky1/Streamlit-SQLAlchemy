import datetime
# import uuid
from random import randint
from typing import Optional

from sqlalchemy import DateTime, Integer, LargeBinary, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = 'Post'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    # uuid: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, nullable=False, default=lambda: (uuid.uuid4().int >> (128 - 32)))
    uuid: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, default=lambda: randint(1, (4_294_967_295)))
    created: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), nullable=False)
    author: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text)
    avatar: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
