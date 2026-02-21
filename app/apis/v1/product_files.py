from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.apis.deps import get_session
from app.schemas.product_file import (
    ProductFileCreate,
    ProductFileUpdate,
    ProductFileResponse,
)
from app.database.crud.product_files import (
    create_product_file,
    get_product_file_by_id,
    get_product_file,
    get_files_for_product,
    update_product_file,
    delete_product_file,
)
from app.core.config import Languages


router = APIRouter(prefix="/product-files")


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------
@router.post("/", response_model=ProductFileResponse, status_code=status.HTTP_201_CREATED)
async def create_file(
    data: ProductFileCreate,
    session: AsyncSession = Depends(get_session)
):
    existing = await get_product_file(session, data.product_id, data.lang)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"File for product {data.product_id} and lang '{data.lang}' already exists"
        )

    return await create_product_file(session, data)


# ---------------------------------------------------------
# GET BY ID
# ---------------------------------------------------------
@router.get("/{file_id}", response_model=ProductFileResponse)
async def read_file_by_id(
    file_id: int,
    session: AsyncSession = Depends(get_session)
):
    file = await get_product_file_by_id(session, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file


# ---------------------------------------------------------
# GET BY PRODUCT + LANG
# ---------------------------------------------------------
@router.get("/by-product/{product_id}/{lang}", response_model=ProductFileResponse)
async def read_file_by_product_and_lang(
    product_id: int,
    lang: Languages,
    session: AsyncSession = Depends(get_session)
):
    file = await get_product_file(session, product_id, lang)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file


# ---------------------------------------------------------
# LIST FILES (optional filter by product_id)
# ---------------------------------------------------------
@router.get("/", response_model=list[ProductFileResponse])
async def list_files(
    product_id: int | None = None,
    session: AsyncSession = Depends(get_session)
):
    if product_id is not None:
        return await get_files_for_product(session, product_id)



# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------
@router.patch("/{file_id}", response_model=ProductFileResponse)
async def update_file(
    file_id: int,
    data: ProductFileUpdate,
    session: AsyncSession = Depends(get_session)
):
    updated = await update_product_file(session, file_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="File not found")
    return updated


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------
@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    file_id: int,
    session: AsyncSession = Depends(get_session)
):
    ok = await delete_product_file(session, file_id)
    if not ok:
        raise HTTPException(status_code=404, detail="File not found")
    return None
