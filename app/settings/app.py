from typing import Optional

from pydantic import BaseSettings, Field, HttpUrl, RedisDsn, SecretStr

from . import base


class BotSettings(BaseSettings):
    TOKEN: SecretStr
    WEBHOOK_HOST: Optional[HttpUrl] = None

    REDIS_URL: Optional[RedisDsn] = None

    class Config:
        env_prefix = 'BOT_'
        env_file = '.env'


class AppSettings(BaseSettings):
    SECRET_KEY: SecretStr

    DATABASE_URL: base.SQLAlchemyPostgresDsn

    LOG_LEVEL: str = Field(default='INFO')

    class Config:
        env_file = '.env'
