from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.database.db import async_session_maker
import base64
import time
import hashlib

from fastapi import Depends, Header, HTTPException, status
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from app.database.models import Admin
from app.database.crud.admin import AdminCRUD
from app.core.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/admin/auth/login")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_current_admin(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        admin_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    admin = await AdminCRUD.get_by_id(session, admin_id)
    if not admin or not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin inactive",
        )

    return admin


# Cripto authorization I do not use it now
# async def verify_access_to_apis(
#         session: AsyncSession = Depends(get_session),
#         x_admin_id: int = Header(..., alias="X-Admin-Id"),
#         x_timestamp: str = Header(..., alias="X-Timestamp"),
#         x_signature: str = Header(..., alias="X-Signature"),
#         request=None,
# ) -> Admin:
#     # 1. Проверяем timestamp
#     now = int(time.time())
#     ts = int(x_timestamp)
#
#     if abs(now - ts) > 60:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Timestamp too old",
#         )
#
#     # 2. Находим администратора
#     admin = await session.get(Admin, x_admin_id)
#     if not admin or not admin.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Admin not found or inactive",
#         )
#
#     # 3. Собираем canonical string
#     body = await request.body()
#     body_hash = hashlib.sha256(body).hexdigest()
#
#     canonical = f"{request.method}\n{request.url.path}\n{x_timestamp}\n{body_hash}"
#
#     # 4. Загружаем публичный ключ
#     public_key = serialization.load_pem_public_key(
#         admin.public_key.encode()
#     )
#
#     if not isinstance(public_key, Ed25519PublicKey):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid public key type",
#         )
#
#     # 5. Проверяем подпись
#     try:
#         public_key.verify(
#             base64.b64decode(x_signature),
#             canonical.encode(),
#         )
#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Invalid signature",
#         )
#
#     return admin
