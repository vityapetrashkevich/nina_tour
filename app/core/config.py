import os
from dotenv import load_dotenv
from typing import Literal

load_dotenv()


class Settings:

    TITLE: str = "SnovaTour API"
    DESCRIPTION: str = "Simple web app for selling tour guides"
    VERSION: str = "1.0.0"

    Languages = Literal["en", "ru", "pl"]

    DATABASE_URL: str = \
        f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    # postgresql://username:password@host:port/database_name

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"

    SECRET_API_KEY: str = os.getenv("PAYMENT_SECRET_API_KEY")


settings: Settings = Settings()
