import os

from pydantic import Field
from pydantic_settings import BaseSettings
import secrets

class RedisConfig(BaseSettings):
    host: str = Field(env="REDIS_HOST", default="0.0.0.0")
    port: int = Field(env="REDIS_PORT", default=6379)
    cache_expire: int | float = Field(env="CACHE_EXPIRE", default=300)


class DBConfig(BaseSettings):
    name: str = Field(env="DB_NAME", default="cinema")
    pg_user: str = Field(env="DB_USER", default="postgres")
    password: str = Field(env="DB_PASSWORD", default="password")
    host: str = Field(env="DB_HOST", default="0.0.0.0")
    port: int = Field(env="DB_PORT", default=5432)
    db_schema: str = Field(env="DB_SCHEMA", default="auth")

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.pg_user}:{self.password}@{self.host}:{self.port}/{self.name}"


class BaseConfig(BaseSettings):
    project_name: str = Field(env="PROJECT_NAME", default="auth_service")
    host: str = Field(env="AUTH_HOST", default="0.0.0.0")
    port: int = Field(env="AUTH_PORT", default="6000")

    middleware_secret_key: str = secrets.token_urlsafe(30)

    db: DBConfig = DBConfig()
    redis_db: RedisConfig = RedisConfig()


settings: BaseConfig = BaseConfig()
