import os

from pydantic import Field
from pydantic_settings import BaseSettings
import secrets


class RedisConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 6379
    cache_expire: int | float = 300

    class Config:
        env_prefix = 'redis_'


class DBConfig(BaseSettings):
    db: str = "cinema"
    user: str = "postgres"
    password: str = "password"
    host: str = "0.0.0.0"
    port: int = 5432

    class Config:
        env_prefix = 'postgres_'

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class BaseConfig(BaseSettings):
    project_name: str = Field(env="PROJECT_NAME", default="auth_service")
    host: str = Field(env="AUTH_HOST", default="0.0.0.0")
    port: int = Field(env="AUTH_PORT", default="6000")

    middleware_secret_key: str = secrets.token_urlsafe(30)
    allow_tracer: bool = True
    allow_request_id: bool = True

    allow_limiter: bool = True

    db: DBConfig = DBConfig()
    redis_db: RedisConfig = RedisConfig()


settings: BaseConfig = BaseConfig()
