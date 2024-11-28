from enum import Enum
from typing import Optional

from pydantic import BaseModel


class AuthorBase(BaseModel):
    id: Optional[int] = None
    first_name: Optional[str] = None
    second_name: Optional[str] = None

    class Config:
        from_attributes = True

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    pass

class AuthorEdit(AuthorBase):
    pass