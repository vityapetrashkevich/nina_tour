from fastapi import APIRouter

from .routes.product import router as product_router
from .routes.thank_you import router as thank_you_router

web_router = APIRouter()

web_router.include_router(product_router)
web_router.include_router(thank_you_router)
