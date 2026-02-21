from typing import List, Optional, Dict, Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.database.models import ProductCardImage
from app.schemas import ProductCardImageCreate, ProductCardImageUpdate, ProductCardImageResponse


async def create_product_card_image(
    session: AsyncSession,
    image_in: ProductCardImageCreate
) -> ProductCardImageResponse:
    """
    Создаёт запись ProductCardImage и возвращает ProductCardImageResponse.
    Откатывает транзакцию при IntegrityError.
    """
    image = ProductCardImage(**image_in.model_dump())
    session.add(image)
    try:
        await session.commit()
        await session.refresh(image)
    except IntegrityError as exc:
        await session.rollback()
        # Можно логировать exc.args
        raise ValueError("Не удалось создать изображение: возможен конфликт или неверные данные") from exc

    return ProductCardImageResponse.model_validate(image.model_dump())


async def get_product_card_image_by_id(
    session: AsyncSession,
    image_id: int
) -> Optional[ProductCardImageResponse]:
    """
    Возвращает ProductCardImageResponse по id или None, если не найдено.
    """
    query = select(ProductCardImage).where(ProductCardImage.id == image_id)
    result = await session.execute(query)
    image = result.scalar_one_or_none()
    if image is None:
        return None
    return ProductCardImageResponse.model_validate(image.model_dump())


async def list_product_card_images(
    session: AsyncSession,
    product_card_id: Optional[int] = None,
    limit: int = 100,
    offset: int = 0
) -> List[ProductCardImageResponse]:
    """
    Возвращает список изображений. Можно фильтровать по product_card_id.
    """
    query = select(ProductCardImage)
    if product_card_id is not None:
        query = query.where(ProductCardImage.product_card_id == product_card_id)
    query = query.offset(offset).limit(limit)

    result = await session.execute(query)
    items = result.scalars().all()
    return [ProductCardImageResponse.model_validate(item.model_dump()) for item in items]


async def update_product_card_image(
    session: AsyncSession,
    image_id: int,
    image_in: ProductCardImageUpdate
) -> Optional[ProductCardImageResponse]:
    """
    Частичное обновление изображения:
    - применяются только поля из image_in (exclude_none=True);
    - id и product_card_id защищены от изменения;
    - возвращает обновлённую Pydantic‑схему или None, если запись не найдена.
    """
    query = select(ProductCardImage).where(ProductCardImage.id == image_id)
    result = await session.execute(query)
    image = result.scalar_one_or_none()
    if image is None:
        return None

    update_data: Dict[str, Any] = image_in.model_dump(exclude_none=True)
    # Защита от изменения ключевых полей
    update_data.pop("id", None)
    update_data.pop("product_card_id", None)

    if not update_data:
        return ProductCardImageResponse.model_validate(image.model_dump())

    for field, value in update_data.items():
        setattr(image, field, value)

    try:
        session.add(image)
        await session.commit()
        await session.refresh(image)
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError("Не удалось обновить изображение: возможен конфликт данных") from exc

    return ProductCardImageResponse.model_validate(image.model_dump())


async def delete_product_card_image(
    session: AsyncSession,
    image_id: int
) -> bool:
    """
    Удаляет изображение по id.
    Возвращает True если удалено, False если не найдено.
    """
    query = select(ProductCardImage).where(ProductCardImage.id == image_id)
    result = await session.execute(query)
    image = result.scalar_one_or_none()
    if image is None:
        return False

    await session.delete(image)
    await session.commit()
    return True
