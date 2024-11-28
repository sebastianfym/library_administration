from typing import List, ClassVar

from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings
from loguru import logger
from pydantic import computed_field, Field

from passlib.context import CryptContext

class SettingsConfig(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class Settings(SettingsConfig):
    ALLOWED_METHODS: List[str] = Field(default_factory=lambda: ["GET", "POST", "PATCH", "DELETE"])
    ALLOWED_HEADERS: List[str] = Field(default_factory=lambda: ["Content-Type", "Authorization", "Accept", "X-Requested-With"])
    ALLOWED_ORIGINS: str = "*"

    SECRET_KEY: str
    REFRESH_TOKEN_EXPIRE_DAYS: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def base_url(self) -> str:
        return f"{self.SERVER_HOST}:{self.SERVER_PORT}"


class PostgresConfig(SettingsConfig):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    @computed_field
    def db_uri(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

class LoggerConfig(BaseSettings):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        logger.add(
            self.LOG_FILE,
            format=self.LOG_FORMAT,
            level=self.LOG_LEVEL,
            rotation=self.LOG_ROTATION,
            compression=self.LOG_COMPRESSION,
            serialize=self.LOG_SERIALIZE
        )

    LOG_FILE: str = "motivation_service.log"
    LOG_FORMAT: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    LOG_LEVEL: str = "DEBUG"
    LOG_ROTATION: str = "10 MB"
    LOG_COMPRESSION: str = "zip"
    LOG_SERIALIZE: bool = True

    logger: ClassVar = logger

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


logger_config = LoggerConfig()
settings = Settings()
postgres_config = PostgresConfig()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"

