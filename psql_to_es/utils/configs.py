from pydantic import BaseSettings, Field, RedisDsn


class PgSettings(BaseSettings):
    dbname: str = Field(env="DB_NAME")
    user: str = Field(env="DB_USER")
    password: str = Field(env="DB_PASSWORD")
    host: str = Field(env="DB_HOST")
    port: str = Field(env="DB_PORT")
    options: str = "-c search_path=content"


class EsSettings(BaseSettings):
    host: str = Field(env="ELASTIC_ADDRESS")


class RedisSettings(BaseSettings):
    host: RedisDsn = Field(env="REDIS_URL")


class BaseConfig(BaseSettings):
    batch_size: int = Field(env="BATCH_SIZE")
    sleep_time: float = Field(env="ETL_SLEEP")
    pg_dsn: PgSettings = PgSettings()
    es_dsn: EsSettings = EsSettings()
    redis_dsn: RedisSettings = RedisSettings()
