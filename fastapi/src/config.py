from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(..., env='PROJECT_NAME')
    DATABASE_URL: str = Field(..., env='DATABASE_URL')

    class Config:
        env_file = '.env'


settings = Settings()
