from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional


from app.database.models import Product, ProductCard
from app.schemas import ProductCreate


async def get_product_with_text_product_code(session, product_code: str, language: str = "en"):
    query = (
        select(Product, ProductCard)
        .join(ProductCard, Product.id == ProductCard.product_id)
        .where(Product.product_code == product_code, ProductCard.lang == language)
    )
    result = await session.execute(query)
    product_row = result.first()
    if not product_row:
        return None
    product, product_text = product_row
    return {**product.dict(), **product_text.dict()}