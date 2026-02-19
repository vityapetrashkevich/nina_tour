from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional


from app.database.models import Order
from app.schemas import OrderSave

async def create_order(
    session: AsyncSession,
    order_in: OrderSave
) -> Order:
    """
    Создаёт продукт и возвращает объект Product
    """
    order = Order(**order_in.model_dump())

    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order




