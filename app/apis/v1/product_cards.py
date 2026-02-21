# app/apis/v1/product_cards.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlmodel.ext.asyncio.session import AsyncSession

from app.apis.deps import get_session
from app.schemas import ProductCardCreate, ProductCardUpdate, ProductCardResponse
from app.database.crud.product_card import (
    create_product_card,
    get_product_card_by_id,
    list_product_cards,
    update_product_card,
    delete_product_card,
)

router = APIRouter(prefix="/product_cards")


# -----------------------------
# CREATE
# -----------------------------
@router.post(
    "",
    response_model=ProductCardResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_product_card_endpoint(
    product_card_in: ProductCardCreate,
    session: AsyncSession = Depends(get_session)
):
    return await create_product_card(session, product_card_in)


# -----------------------------
# READ BY ID
# -----------------------------
@router.get(
    "/{product_card_id}",
    response_model=ProductCardResponse
)
async def get_product_card_endpoint(
    product_card_id: int,
    session: AsyncSession = Depends(get_session)
):
    product_card = await get_product_card_by_id(session, product_card_id)
    if not product_card:
        raise HTTPException(status_code=404, detail="ProductCard not found")
    return product_card


# -----------------------------
# LIST
# -----------------------------
@router.get(
    "",
    response_model=List[ProductCardResponse]
)
async def list_product_cards_endpoint(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session)
):
    return await list_product_cards(session, limit=limit, offset=offset)


# -----------------------------
# UPDATE (PATCH)
# -----------------------------
@router.patch(
    "/{product_card_id}",
    response_model=ProductCardResponse
)
async def update_product_card_endpoint(
    product_card_id: int,
    product_card_in: ProductCardUpdate,
    session: AsyncSession = Depends(get_session)
):
    updated = await update_product_card(session, product_card_id, product_card_in)
    if updated is None:
        raise HTTPException(status_code=404, detail="ProductCard not found")
    return updated


# -----------------------------
# DELETE
# -----------------------------
@router.delete(
    "/{product_card_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product_card_endpoint(
    product_card_id: int,
    session: AsyncSession = Depends(get_session)
):
    deleted = await delete_product_card(session, product_card_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="ProductCard not found")
    return None
