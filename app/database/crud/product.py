from typing import List, Optional, Dict, Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.database.models import Product
from app.schemas import ProductCreate, ProductUpdate


async def create_product(
    session: AsyncSession,
    product_in: ProductCreate
) -> Product:
    """
    Создаёт продукт и возвращает объект Product.
    Проверяет уникальность product_code и аккуратно откатывает транзакцию при ошибке.
    """
    product = Product(**product_in.model_dump())
    session.add(product)
    try:
        await session.commit()
        await session.refresh(product)
        return product
    except IntegrityError as exc:
        await session.rollback()
        # IntegrityError может означать нарушение уникальности product_code
        raise ValueError("Не удалось создать продукт: возможен конфликт уникальности") from exc


async def get_product_by_id(
    session: AsyncSession,
    product_id: int
) -> Optional[Product]:
    """
    Получение продукта по id.
    """
    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_product_by_code(
    session: AsyncSession,
    product_code: str
) -> Optional[Product]:
    """
    Получение продукта по product_code.
    """
    query = select(Product).where(Product.product_code == product_code)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_product_by_ids(
    session: AsyncSession,
    product_id: Optional[int] = None,
    product_code: Optional[str] = None
) -> Optional[Product]:
    """
    Удобная обёртка: ищет по id, если не указан — по product_code.
    Возвращает None, если ни один параметр не передан или продукт не найден.
    """
    if product_id is not None:
        return await get_product_by_id(session, product_id)
    if product_code is not None:
        return await get_product_by_code(session, product_code)
    return None


async def list_products(
    session: AsyncSession,
    limit: int = 100,
    offset: int = 0
) -> List[Product]:
    """
    Получение списка продуктов с лимитом и смещением.
    """
    query = select(Product).offset(offset).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


async def update_product(
    session: AsyncSession,
    product_id: int,
    product_in: ProductUpdate
) -> Optional[Product]:
    """
    Частичное обновление продукта.
    - product_in содержит опциональные поля; применяются только непустые (exclude_none=True).
    - id нельзя обновлять.
    Возвращает обновлённый объект или None, если продукт не найден.
    """
    product = await get_product_by_id(session, product_id)
    if product is None:
        return None

    update_data: Dict[str, Any] = product_in.model_dump(exclude_none=True)
    if not update_data:
        # Нечего обновлять
        return product

    for field, value in update_data.items():
        setattr(product, field, value)

    try:
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError("Не удалось обновить продукт: возможен конфликт уникальности") from exc


async def delete_product(
    session: AsyncSession,
    product_id: int
) -> bool:
    """
    Удаляет продукт по id.
    Возвращает True, если удаление выполнено, False если продукт не найден.
    """
    product = await get_product_by_id(session, product_id)
    if product is None:
        return False

    await session.delete(product)
    await session.commit()
    return True
