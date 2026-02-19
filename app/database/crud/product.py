from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional


from app.database.models import Product
from app.schemas import ProductCreate


async def create_product(
    session: AsyncSession,
    product_in: ProductCreate
) -> Product:
    """
    Создаёт продукт и возвращает объект Product
    """
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product



async def get_product_by_ids(
    session: AsyncSession,
    product_id: Optional[int] = None,
    product_code: Optional[str] = None
) -> Optional[Product]:
    """
    Получение продукта по id или product_code
    """
    query = select(Product)
    if product_id is not None:
        query = query.where(Product.id == product_id)
    elif product_code is not None:
        query = query.where(Product.product_code == product_code)
    else:
        return None

    result = await session.execute(query)
    return result.scalar_one_or_none()


async def list_products(
    session: AsyncSession,
    limit: int = 100,
    offset: int = 0
) -> List[Product]:
    """
    Получение списка продуктов с лимитом и смещением
    """
    query = select(Product).offset(offset).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()

