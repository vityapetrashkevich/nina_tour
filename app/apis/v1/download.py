from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlmodel.ext.asyncio.session import AsyncSession
import os

from app.apis.deps import get_session
from app.database.crud.product_files import get_product_file_by_id
from app.core.config import Languages

router = APIRouter(prefix="/download")


@router.get("/{id}")
async def download_file(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    # 1. Получаем продукт
    file = await get_product_file_by_id(session, id)
    if not file:
        raise HTTPException(status_code=404, detail="File for this language not found")

    # 3. Формируем путь
    # file.file_link хранит относительный путь, например: "files/paris_ru.pdf"
    static_root = "app/web"
    full_path = os.path.join(static_root, file.file_link.lstrip("/"))

    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found on server")

    # 4. Отдаём файл безопасно
    return FileResponse(
        full_path,
        filename=os.path.basename(full_path),
        media_type="application/pdf"
    )
