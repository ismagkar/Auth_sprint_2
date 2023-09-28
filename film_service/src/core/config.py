import os

from pydantic import BaseSettings, Field


class RedisConfig(BaseSettings):
    host: str = Field(env="REDIS_HOST", default="0.0.0.0")
    port: int = Field(env="REDIS_PORT", default=6379)
    cache_expire: int | float = Field(env="CACHE_EXPIRE", default=300)


class ElasticConfig(BaseSettings):
    host: str = Field(env="ELASTIC_HOST", default="0.0.0.0")
    port: int = Field(env="ELASTIC_PORT", default=9200)

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}/"


class BaseConfig(BaseSettings):
    project_name: str = Field(env="PROJECT_NAME", default="movies")
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    host: str = Field(env="FAST_API_HOST", default="0.0.0.0")
    port: int = Field(env="FAST_API_PORT", default=8888)

    redis: RedisConfig = RedisConfig()
    elastic: ElasticConfig = ElasticConfig()


settings: BaseConfig = BaseConfig()
