from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlmodel.ext.asyncio.session import AsyncSession
import httpx
import json
import logging

from app.core.config import settings
from app.apis.deps import get_session
from app.schemas import OrderCreate, OrderSave, OrderRead
from app.database.crud.product import get_product_by_ids
from app.database.crud.order import create_order, get_order_by_id, list_orders, list_orders_by_status

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/order")


@router.post(
    "",
    status_code=status.HTTP_200_OK
)
async def create_order_api(
    order_in: OrderCreate,
    session: AsyncSession = Depends(get_session),
):
    """
    Создаёт заказ: 1) проверяет продукт, 2) вызывает провайдера платежей, 3) сохраняет заказ в БД.
    Возвращает OrderSave (token/checkout_url помечены exclude=True в схеме, но checkout_url
    возвращается эпhemerally в поле checkout_url_response).
    """
    # 1) Проверяем продукт
    product = await get_product_by_ids(session, product_code=order_in.product_code)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # 2) Формируем запрос к провайдеру
    try:
        url = settings.REVOLUT_URL + "/api/orders"
    except AttributeError as e:
        print(settings)
    payload = {
        "amount": product.price,
        "currency": product.currency,
        "settlement_currency": order_in.settlement_currency,
        "customer": {"email": order_in.customers_email},
        "metadata": {"product_code": order_in.product_code, "product_lang": order_in.lang},
        "redirect_url": f'{settings.MY_URL}/thank-you/{order_in.product_code}/{order_in.lang.value}',
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        # Используем ключ из Settings, если он не задан — логируем и возвращаем 500
        "Authorization": f"Bearer {settings.SECRET_API_KEY}" if getattr(settings, "SECRET_API_KEY", None) else "",
        'Revolut-Api-Version': settings.Revolut_Api_Version,
    }
    if not headers["Authorization"]:
        logger.error("Payment provider API key is not configured (Settings.SECRET_API_KEY missing)")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Payment provider not configured")

    # 3) Вызов провайдера
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(url, headers=headers, json=payload)
        except httpx.HTTPError as exc:
            logger.exception("HTTP error while calling payment provider")
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Payment provider unreachable") from exc

    # 4) Обработка ответа провайдера
    if resp.status_code != status.HTTP_201_CREATED:
        logger.error("Payment provider returned error: %s %s", resp.status_code, resp.text)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Error in payment system side")

    provider_data = resp.json()

    # 5) Формируем объект для сохранения в БД.
    #    Важно: token/checkout_url не сохраняем в БД (игнорируем при сохранении),
    #    но можем вернуть checkout_url клиенту в ответе (ephemeral).
    #    Предполагаем, что create_order CRUD умеет принять dict/Pydantic с нужными полями.
    order = OrderSave(
        **order_in.model_dump(exclude={"settlement_currency"}),
        **provider_data
    )

    # 6) Сохраняем заказ в БД
    # try:
        # create_order — твоя CRUD функция; она должна вернуть OrderSave (или None/raise)
    saved_order = await create_order(session, order)
    # except ValueError as exc:
    #     logger.exception("Failed to save order to DB")
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

    if not saved_order:
        logger.error("create_order returned falsy value")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Order creation failed")

    # 7) Возвращаем сохранённый заказ. Если нужно — возвращаем checkout_url отдельно (ephemeral)
    #    OrderSave.schema помечает checkout_url exclude=True, поэтому добавим его вручную в ответ payload
    checkout_url = provider_data.get("checkout_url")
    return {"url": checkout_url}


@router.get("/{order_id}", response_model=OrderRead)
async def get_order_api(order_id: str = Path(..., description="Order id"), session: AsyncSession = Depends(get_session)):
    order = await get_order_by_id(session, order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.get("/", response_model=List[OrderRead])
async def list_orders_api(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session)
):
    return await list_orders(session, limit=limit, offset=offset)


@router.get("/by-status/{status}", response_model=List[OrderRead])
async def list_orders_by_status_api(
    status: str,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session)
):
    return await list_orders_by_status(session, status=status, limit=limit, offset=offset)
