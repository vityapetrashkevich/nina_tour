from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict
from sqlalchemy import text

from app.apis.deps import get_session

router = APIRouter(prefix="/service")

@router.get("/ping")
async def ping() -> Dict[str, str]:
    return {"message": "Hello World"}


@router.get("/health/db", response_model=Dict[str, str], status_code=status.HTTP_200_OK)
async def health_check_db() -> Dict[str, str]:
    try:
        async for db in get_session():  # <- здесь async for
            await db.execute(text("SELECT 1"))
            break  # нужен только один раз
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
