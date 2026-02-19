import jwt
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.database.db import async_engine, async_session_maker
from app.core.config import settings


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session