from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from app.apis.deps import get_session
from app.schemas import ProductCreate, ProductResponse
from app.database.crud.product import create_product, get_product_by_ids, list_products


router = APIRouter(prefix="/products")

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
            status_code=400,
            detail="Product with this product_code already exists"
        )

    return await create_product(session, product_in)



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


@router.get(
    "",
    response_model=List[ProductResponse]
)
async def list_products_endpoint(
    limit: int = 100,
    offset: int = 0,
    session: AsyncSession = Depends(get_session)
):
    return await list_products(session, limit=limit, offset=offset)

