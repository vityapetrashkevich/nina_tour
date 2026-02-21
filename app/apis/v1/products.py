from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlmodel.ext.asyncio.session import AsyncSession

from app.apis.deps import get_session
from app.schemas import ProductCreate, ProductUpdate, ProductResponse
from app.database.crud.product import create_product, get_product_by_ids, list_products, update_product, delete_product

router = APIRouter(prefix="/products")


# -----------------------------
# CREATE
# -----------------------------
@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_product_endpoint(
    product_in: ProductCreate,
    session: AsyncSession = Depends(get_session)
):
    existing = await get_product_by_ids(
        session,
        product_code=product_in.product_code
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product with this product_code already exists"
        )

    try:
        return await create_product(session, product_in)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


# -----------------------------
# READ BY ID
# -----------------------------
@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
async def get_product_by_id(
    product_id: int,
    session: AsyncSession = Depends(get_session)
):
    product = await get_product_by_ids(session, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# -----------------------------
# LIST
# -----------------------------
@router.get(
    "",
    response_model=List[ProductResponse]
)
async def list_products_endpoint(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session)
):
    return await list_products(session, limit=limit, offset=offset)


# -----------------------------
# UPDATE (PATCH)
# -----------------------------
@router.patch(
    "/{product_id}",
    response_model=ProductResponse
)
async def update_product_endpoint(
    product_id: int,
    product_in: ProductUpdate,
    session: AsyncSession = Depends(get_session)
):
    updated = await update_product(session, product_id, product_in)
    if updated is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


# -----------------------------
# DELETE
# -----------------------------
@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product_endpoint(
    product_id: int,
    session: AsyncSession = Depends(get_session)
):
    deleted = await delete_product(session, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
