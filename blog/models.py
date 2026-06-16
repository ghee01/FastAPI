from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from database.orm import Base

class Blog(Base):
    __tablename__ = 'blog'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    content: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )