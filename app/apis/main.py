from fastapi import APIRouter

from .v1.products import router as product_router
from .v1.product_cards import router as cards_router
from .v1.service import router as service_router
from .v1.order import router as order_router

api_router = APIRouter()
api_router.include_router(service_router, prefix="/v1", tags=["Service"])
api_router.include_router(product_router, prefix="/v1", tags=["Product"])
api_router.include_router(cards_router, prefix="/v1", tags=["Product Cards"])
api_router.include_router(order_router, prefix="/v1", tags=["Order"])
