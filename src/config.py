import os

from dotenv import find_dotenv, load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict




class Settings(BaseSettings):
    MODE: str

    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int
    REDIS_HOST: str
    REDIS_PORT: int
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def REDIS_URL(self):
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'

    model_config = SettingsConfigDict(env_file=".env")


load_dotenv(find_dotenv(".env"))
settings = Settings()
