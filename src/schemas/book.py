from typing import Optional

from pydantic import BaseModel

from src.enums.enum import BookStatus
from src.schemas.author import Author


class BookBase(BaseModel):
    id: Optional[int] = None
    year: Optional[int] = None
    title: Optional[str] = None
    status: Optional[str] = None
    author_id: Optional[int] = None

    class Config:
        use_enum_values = True
        from_attributes = True


class BookCreate(BookBase):
    pass

class Book(BookBase):
    pass

class BookEdit(BookBase):
    status: BookStatus = None

class BookDetail(BookBase):
    author: Optional[Author] = None