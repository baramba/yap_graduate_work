from logging import config as logging_config
import logstash
from pydantic import (BaseSettings, Field)

from config.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class PostgresDsn(BaseSettings):
    dbname: str = Field('graduate', env='DB_NAME')
    user: str = Field('app', env='POSTGRES_USER')
    password: str = Field('123qwe', env='POSTGRES_PASSWORD')
    host: str = Field('127.0.0.1', env='POSTGRES_SERVER')
    port: str = Field(5432, env='POSTGRES_PORT')


class Settings(BaseSettings):
    MAX_IN_RECORDS_DB: int = Field(1000, env='MAX_IN_RECORDS_DB')
    CREATED_BY: int = Field(1, env='CREATED_BY')
    HOST: str = Field('127.0.0.1', env='HOST_FLASK')
    REDIS_HOST:  str = Field('127.0.0.1', env='REDIS_HOST')
    REDIS_PORT:  str = Field('6379', env='REDIS_PORT')

settings = Settings()
