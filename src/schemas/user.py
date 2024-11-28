from typing import Optional

from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class UserAuthSchema(BaseModel):
    username: str
    password: str


class TokenRefreshRequestSchema(BaseModel):
    refresh_token: str

class UserCreate(BaseModel):
    username: str
    password: str
