from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional

from app.database.models import ProductCard
from app.schemas import ProductCardCreate


async def create_product_card(
    session: AsyncSession,
    product_text_in: ProductCardCreate
) -> ProductCard:
    product_card = ProductCard(**product_text_in.model_dump())

    session.add(product_card)
    await session.commit()
    await session.refresh(product_card)

    return product_card


async def get_product_card_by_id(
    session: AsyncSession,
    product_text_id: int
) -> Optional[ProductCard]:
    result = await session.execute(
        select(ProductCard).where(ProductCard.id == product_text_id)
    )
    return result.scalar_one_or_none()

async def get_all_product_cards(session: AsyncSession, limit: int = 100, offset: int = 0) -> List[ProductCard]:
    result = await session.execute(select(ProductCard).offset(offset).limit(limit))
    return result.scalars().all()

