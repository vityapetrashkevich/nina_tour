from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.system_metadata import SystemMetadata


class SystemMetaCRUD:
    @staticmethod
    async def get_value(session: AsyncSession, key: str) -> str | None:
        obj = await session.get(SystemMetadata, key)
        return obj.value if obj else None

    @staticmethod
    async def set_value(session: AsyncSession, key: str, value: str) -> None:
        obj = await session.get(SystemMetadata, key)
        if obj:
            obj.value = value
        else:
            session.add(SystemMetadata(key=key, value=value))
