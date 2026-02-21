# from sqlmodel import create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

print(f"DATABASE_URL is: {settings.DATABASE_URL}")

# engine = create_engine(settings.DATABASE_URL)

async_engine = create_async_engine(
    settings.DATABASE_URL, echo=True, pool_pre_ping=True
)

async_session_maker = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
