from typing import List, Optional, Dict, Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.database.models import ProductCard
from app.schemas import ProductCardCreate, ProductCardUpdate, ProductCardResponse


async def create_product_card(
    session: AsyncSession,
    product_card_in: ProductCardCreate
) -> ProductCardResponse:
    """
    Создаёт ProductCard и возвращает Pydantic-схему ProductCardResponse.
    Обрабатывает конфликт уникальности (product_id, lang).
    """
    product_card = ProductCard(**product_card_in.model_dump())
    session.add(product_card)
    try:
        await session.commit()
        await session.refresh(product_card)
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError("Не удалось создать карточку: возможен конфликт уникальности (product_id, lang)") from exc

    # Конвертация в Pydantic-схему
    return ProductCardResponse.model_validate(product_card.model_dump())


async def get_product_card_by_id(
    session: AsyncSession,
    product_card_id: int
) -> Optional[ProductCardResponse]:
    """
    Получение ProductCard по id. Возвращает Pydantic-схему или None.
    """
    query = select(ProductCard).where(ProductCard.id == product_card_id)
    result = await session.execute(query)
    product_card = result.scalar_one_or_none()
    if product_card is None:
        return None
    return ProductCardResponse.model_validate(product_card.model_dump())


async def get_product_card_by_product_and_lang(
    session: AsyncSession,
    product_id: int,
    lang: str
) -> Optional[ProductCardResponse]:
    """
    Получение ProductCard по product_id и lang.
    """
    query = select(ProductCard).where(
        ProductCard.product_id == product_id,
        ProductCard.lang == lang
    )
    result = await session.execute(query)
    product_card = result.scalar_one_or_none()
    if product_card is None:
        return None
    return ProductCardResponse.model_validate(product_card.model_dump())


async def list_product_cards(
    session: AsyncSession,
    product_id: Optional[int] = None,
    lang: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
) -> List[ProductCardResponse]:
    """
    Список карточек с опциональной фильтрацией по product_id и lang.
    Возвращает список Pydantic-схем.
    """
    query = select(ProductCard)
    if product_id is not None:
        query = query.where(ProductCard.product_id == product_id)
    if lang is not None:
        query = query.where(ProductCard.lang == lang)
    query = query.offset(offset).limit(limit)

    result = await session.execute(query)
    items = result.scalars().all()
    return [ProductCardResponse.model_validate(item.model_dump()) for item in items]


async def update_product_card(
    session: AsyncSession,
    product_card_id: int,
    product_card_in: ProductCardUpdate
) -> Optional[ProductCardResponse]:
    """
    Частичное обновление ProductCard.
    - Применяются только поля из product_card_in (exclude_none=True).
    - id и product_id не обновляются через этот метод.
    Возвращает обновлённую Pydantic‑схему или None, если не найдено.
    """
    query = select(ProductCard).where(ProductCard.id == product_card_id)
    result = await session.execute(query)
    product_card = result.scalar_one_or_none()
    if product_card is None:
        return None

    update_data: Dict[str, Any] = product_card_in.model_dump(exclude_none=True)
    # Защита от изменения ключевых полей
    update_data.pop("id", None)
    update_data.pop("product_id", None)

    if update_data:
        for field, value in update_data.items():
            setattr(product_card, field, value)

        try:
            session.add(product_card)
            await session.commit()
            await session.refresh(product_card)
        except IntegrityError as exc:
            await session.rollback()
            raise ValueError("Не удалось обновить карточку: возможен конфликт уникальности") from exc

    return ProductCardResponse.model_validate(product_card.model_dump())


async def delete_product_card(
    session: AsyncSession,
    product_card_id: int
) -> bool:
    """
    Удаляет ProductCard по id.
    Возвращает True если удалено, False если не найдено.
    """
    query = select(ProductCard).where(ProductCard.id == product_card_id)
    result = await session.execute(query)
    product_card = result.scalar_one_or_none()
    if product_card is None:
        return False

    await session.delete(product_card)
    await session.commit()
    return True
