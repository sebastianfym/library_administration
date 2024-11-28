import decimal

from sqlalchemy import String, DateTime, Integer, Float, ForeignKey, text, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.database import Base
from src.enums.enum import BookStatus


class Author(Base):
    __tablename__ = "author"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, unique=True)
    first_name: Mapped[String] = mapped_column(String(100), nullable=False)
    second_name: Mapped[String] = mapped_column(String(100), index=True, nullable=False)

    books: Mapped["Book"] = relationship("Book", back_populates="author", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "book"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, unique=True)
    year: Mapped[Integer] = mapped_column(Integer, default=2024, nullable=False)
    title: Mapped[String] = mapped_column(String(100), unique=False, index=True, nullable=False)
    status: Mapped[String] = mapped_column(String(10), unique=False, index=True, nullable=True, default=BookStatus.ISSUED.value)

    author_id: Mapped[Integer] = mapped_column(ForeignKey("author.id"), nullable=False)
    author: Mapped["Author"] = relationship("Author", back_populates="books", lazy="joined")