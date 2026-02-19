from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from app.apis.deps import get_session
from app.schemas import ProductCardCreate, ProductCardResponse
from app.database.crud.product_card import create_product_card, get_product_card_by_id, get_all_product_cards

router = APIRouter(prefix="/product_cards")

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


@router.get(
    "",
    response_model=List[ProductCardResponse]
)
async def list_product_cards_endpoint(
    limit: int = 100,
    offset: int = 0,
    session: AsyncSession = Depends(get_session)
):
    return await get_all_product_cards(session, limit=limit, offset=offset)
