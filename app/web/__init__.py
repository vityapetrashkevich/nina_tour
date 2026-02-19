from fastapi import APIRouter

from .routes.product import router as product_router

web_router = APIRouter()

web_router.include_router(product_router)
