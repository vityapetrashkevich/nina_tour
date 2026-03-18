from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import get_password_hash, generate_secure_password
from app.database.models import Admin
from app.schemas.admins import AdminRegisterRequest, AdminUpdateRequest


class AdminCRUD:
    @staticmethod
    async def get_by_id(session: AsyncSession, id: int) -> Optional[Admin]:
        return await session.get(Admin, id)

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> Optional[Admin]:
        statement = select(Admin).where(Admin.email == email)
        result = await session.execute(statement)
        return result.scalar_one_or_none()


    @staticmethod
    async def create(session: AsyncSession, data: AdminRegisterRequest, init=False) -> (Admin, str):
        password = generate_secure_password()
        new_row = Admin(email=data.email, password_hash=get_password_hash(password),
                        public_key_pem=data.public_key, is_active=True, )
        session.add(new_row)
        if not init:
            try:
                await session.commit()
                await session.refresh(new_row)
            except Exception:  # Если email уже существует — БД сама выбросит ошибку unique constraint
                await session.rollback()
                raise
        return new_row, password

    @staticmethod
    async def update(session: AsyncSession, data: AdminUpdateRequest) ->Admin:
        if (not data.password) and (not data.public_key):
            raise ValueError("Nothing to update")
        else:
            admin = await AdminCRUD.get_by_id(session, data.id)
            if data.password:
                admin.password_hash = get_password_hash(data.password)
            if data.public_key:
                admin.public_key = data.public_key
        session.add(admin)
        await session.commit()
        await session.refresh(admin)
        return admin

    @staticmethod
    async def deactivate(session: AsyncSession, id:int) -> Admin:
        admin = await AdminCRUD.get_by_id(session, id)
        admin.is_active = False
        session.add(admin)
        await session.commit()
        await session.refresh(admin)
        return admin
