import datetime
from typing import Optional

from sqlalchemy import Integer, DateTime, LargeBinary, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = 'Post'

    # id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, default=lambda: (uuid.uuid4().int >> (128 - 32)))
    # uuid: Mapped[int] = mapped_column(Integer, unique=True, default=lambda: randint(1, (4_294_967_295)))
    uuid: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    author: Mapped[str] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text)
    content: Mapped[Optional[str]] = mapped_column(Text)
    avatar: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
