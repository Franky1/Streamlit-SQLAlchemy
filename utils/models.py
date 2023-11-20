from typing import Optional

from sqlalchemy import DateTime, LargeBinary, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime

class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = 'Post'

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    author: Mapped[str] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text)
    avatar: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    content: Mapped[Optional[str]] = mapped_column(Text)
