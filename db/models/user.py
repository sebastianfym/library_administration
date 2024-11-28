from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey

from db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "user"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String(55), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, unique=True)
    token: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    user_id: Mapped[Integer] = mapped_column(ForeignKey("user.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user = relationship("User", back_populates="refresh_token")