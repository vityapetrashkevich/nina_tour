from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.database.models import Order
from app.schemas import OrderUpdate, OrderSave, OrderRead


async def create_order(
    session: AsyncSession,
    order_in: OrderSave
) -> bool:
    """
    Создаёт заказ и возвращает OrderSave.
    - Игнорируем любые token/checkout_url (не сохраняем в БД).
    """
    # Берём только поля из схемы OrderCreate (token/checkout_url там не определены)
    order = Order(**order_in.model_dump())
    session.add(order)
    try:
        await session.commit()
        await session.refresh(order)
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError("Не удалось создать заказ: возможен конфликт данных") from exc

    return True


async def get_order_by_id(
    session: AsyncSession,
    order_id: str
) -> Optional[OrderRead]:
    query = select(Order).where(Order.id == order_id)
    result = await session.execute(query)
    order = result.scalar_one_or_none()
    if order is None:
        return None
    return OrderRead.model_validate(order.model_dump())


async def list_orders(
    session: AsyncSession,
    limit: int = 100,
    offset: int = 0
) -> List[OrderRead]:
    query = select(Order).offset(offset).limit(limit)
    result = await session.execute(query)
    items = result.scalars().all()
    return [OrderRead.model_validate(item.model_dump()) for item in items]


async def list_orders_by_status(
    session: AsyncSession,
    status: str,
    limit: int = 100,
    offset: int = 0
) -> List[OrderRead]:
    query = select(Order).where(Order.state == status).offset(offset).limit(limit)
    result = await session.execute(query)
    items = result.scalars().all()
    return [OrderRead.model_validate(item.model_dump()) for item in items]


async def list_orders_by_product(
    session: AsyncSession,
    product_code: Optional[str] = None,
    product_id: Optional[int] = None,
    limit: int = 100,
    offset: int = 0
) -> List[OrderRead]:
    query = select(Order)
    if product_id is not None:
        query = query.where(Order.product_id == product_id)
    elif product_code is not None:
        query = query.where(Order.product_code == product_code)
    else:
        return []

    query = query.offset(offset).limit(limit)
    result = await session.execute(query)
    items = result.scalars().all()
    return [OrderRead.model_validate(item.model_dump()) for item in items]


async def update_order(
    session: AsyncSession,
    order_id: str,
    order_in: OrderUpdate
) -> Optional[OrderRead]:
    """
    Частичное обновление заказа.
    - Применяются только поля из order_in (exclude_none=True).
    - id не обновляется.
    - token и checkout_url игнорируются (не сохраняются).
    - updated_at устанавливается в текущее UTC время перед коммитом.
    """
    query = select(Order).where(Order.id == order_id)
    result = await session.execute(query)
    order = result.scalar_one_or_none()
    if order is None:
        return None

    update_data: Dict[str, Any] = order_in.model_dump(exclude_none=True)

    # Защита: не позволяем менять id
    update_data.pop("id", None)

    # Игнорируем token/checkout_url — они не сохраняются в БД
    update_data.pop("token", None)
    update_data.pop("checkout_url", None)

    if not update_data:
        # Обновляем только updated_at, чтобы отразить факт обращения (если нужно)
        order.updated_at = datetime.now(timezone.utc)
        try:
            session.add(order)
            await session.commit()
            await session.refresh(order)
        except IntegrityError:
            await session.rollback()
            raise ValueError("Не удалось обновить заказ: возможен конфликт данных")
        return OrderSave.model_validate(order.model_dump())

    # Применяем изменения
    for field, value in update_data.items():
        setattr(order, field, value)

    # Обновляем updated_at автоматически
    order.updated_at = datetime.now(timezone.utc)

    try:
        session.add(order)
        await session.commit()
        await session.refresh(order)
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError("Не удалось обновить заказ: возможен конфликт данных") from exc

    return OrderRead.model_validate(order.model_dump())
