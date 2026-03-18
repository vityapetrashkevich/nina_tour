from pydantic_settings import BaseSettings
from pydantic import Field, computed_field
from passlib.context import CryptContext
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
    INIT_DATA_FILE: ClassVar[str] = 'app/init_data.yaml'
    ACCESS_TOKEN_EXPIRE_MINUTES: ClassVar[int] = 30
    bcrypt_schemes: list[str] = ["bcrypt"]
    bcrypt_deprecated: str = "auto"

    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: int = Field(..., env="DB_PORT")
    DB_NAME: str = Field(..., env="DB_NAME")
    REVOLUT_URL: str = Field(..., env="REVOLUT_URL")
    SECRET_KEY: str = Field(env="JWT_SECRET_KEY", default='wispcwtoypfwknhop')
    SECRET_API_KEY: str = Field(..., env="SECRET_API_KEY")
    #SECRET_API_KEY: str = Field(..., validation_alias="PAYMENT_KEY")
    MY_URL: str = Field(default="localhost:8001", env="MY_URL")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._crypt_context = CryptContext(
            schemes=self.bcrypt_schemes,
            deprecated=self.bcrypt_deprecated,
        )

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def crypt_context(self) -> CryptContext:
            return self._crypt_context


settings = Settings()
