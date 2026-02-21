from typing import Optional, List, Dict

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models import Product, ProductCard, ProductCardImage
from app.schemas import ProductWithCardResponse, ProductCardImageResponse


async def get_product_with_card_by_code(
    session: AsyncSession,
    product_code: str,
    lang: str
) -> Optional[ProductWithCardResponse]:
    """
    Возвращает объединённую запись product + card (по lang) и массив изображений.
    Если пара (product_code, lang) не найдена — возвращает None.
    Выполняет три батч‑запроса: product, card, images.
    """
    # 1) product
    q_prod = select(Product).where(Product.product_code == product_code)
    result = await session.execute(q_prod)
    product_obj = result.scalar_one_or_none()
    if product_obj is None:
        return None

    product_id = product_obj.id

    # 2) card по product_id и lang (lang обязателен)
    q_card = select(ProductCard).where(
        ProductCard.product_id == product_id,
        ProductCard.lang == lang
    )
    result = await session.execute(q_card)
    card_obj = result.scalar_one_or_none()
    if card_obj is None:
        # карточки для данного языка нет — возвращаем None (по бизнес‑логике)
        return None

    # 3) изображения для найденной карточки (batch)
    q_images = select(ProductCardImage).where(ProductCardImage.product_card_id == card_obj.id)
    result = await session.execute(q_images)
    images: List[ProductCardImage] = result.scalars().all()

    # 4) подготовка payload для ProductWithCardResponse
    images_schema = [ProductCardImageResponse.model_validate(img.model_dump()) for img in images]

    payload = {
        # product
        "product_id": product_obj.id,
        "product_code": product_obj.product_code,
        "title": getattr(product_obj, "title", None),
        "price": getattr(product_obj, "price", None),
        "currency": getattr(product_obj, "currency", None),
        "product_created_at": getattr(product_obj, "created_at", None),
        "product_updated_at": getattr(product_obj, "updated_at", None),

        # card
        "card_id": card_obj.id,
        "lang": card_obj.lang,
        "name": card_obj.name,
        "description": card_obj.description,
        "card_created_at": getattr(card_obj, "created_at", None),
        "card_updated_at": getattr(card_obj, "updated_at", None),

        # images
        "images": images_schema,
    }

    return ProductWithCardResponse.model_validate(payload)
