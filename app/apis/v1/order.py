from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession

import httpx
import json


from app.core.config import Settings
from app.apis.deps import get_session
from app.schemas import OrderCreate, OrderSave
from app.database.crud.product import get_product_by_ids
from app.database.crud.order import create_order

router = APIRouter(prefix="/order")


@router.post(
    "",
    # response_model=ProductResponse,
    status_code=status.HTTP_200_OK
)
async def create_order_api(
        order_in: OrderCreate,
        session: AsyncSession = Depends(get_session)
):
    product = await get_product_by_ids(session, product_code=order_in.product_code)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    url = "https://sandbox-merchant.revolut.com/api/orders"

    payload = json.dumps({
        "amount": product.price,
        "currency": product.currency,
        'settlement_currency': order_in.settlement_currency,
        'customer': {
            "email": order_in.customers_email
        },
        "metadata": {
            "product_code": order_in.product_code,
            'product_lang': order_in.lang
        },
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer sk_Y8QHgxhMKheVnH6X6wOcHlOm3_ZpwQCvFs3OCTu478iLzWYvR4rp82bW7KJ8SdVs',# + Settings.SECRET_API_KEY,
        'Revolut-Api-Version': '2025-12-04'
    }
    print(headers)
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=payload)
    if response.status_code == status.HTTP_201_CREATED:
        print(order_in.model_dump(exclude={"settlement_currency"}))
        print(type(order_in))
        print(response.json())
        order = OrderSave(
              **order_in.model_dump(exclude={"settlement_currency"}),
              **response.json()
        )
        o = await create_order(session, order)
        if not o:
            raise HTTPException(400, detail="Order creation failed")
        return { "url": order.checkout_url }
    else:
        print(response)
        raise HTTPException(status_code=500, detail="Error in payment system side")

