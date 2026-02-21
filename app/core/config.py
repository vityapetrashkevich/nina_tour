from pydantic_settings import BaseSettings
from pydantic import Field, computed_field
from typing import ClassVar
from enum import Enum


class Currency(str, Enum):
    USD = 'USD'
    EUR = 'EUR'
    PLN = 'PLN'
    GBP = 'GBP'
    CZK = 'CZK'


class Languages(str, Enum):
    en = "en"
    ru = "ru"
    pl = "pl"


class Settings(BaseSettings):
    TITLE: ClassVar[str] = "SnovaTour API"
    DESCRIPTION: ClassVar[str] = "Simple web app for selling tour guides"
    VERSION: ClassVar[str] = "1.0.0"
    Revolut_Api_Version: ClassVar[str] = '2025-12-04'
    ALGORITHM: ClassVar[str] = "HS256"

    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: int = Field(..., env="DB_PORT")
    DB_NAME: str = Field(..., env="DB_NAME")
    REVOLUT_URL: str = Field(..., env="REVOLUT_URL")
    # SECRET_API_KEY: str = Field(..., env="PAYMENT_KEY")
    SECRET_API_KEY: str = Field(..., validation_alias="PAYMENT_KEY")

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
