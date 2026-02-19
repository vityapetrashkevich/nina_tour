from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.templating import Jinja2Templates

from app.apis.deps import get_session
from app.database.crud.product_with_cards import get_product_with_text_product_code


router = APIRouter(prefix="/products")
templates = Jinja2Templates(directory="app/web/templates")

@router.get("/{lang}/{product_code}")
async def product_page(request: Request, product_code: str, lang: str = "en",
                       session: AsyncSession = Depends(get_session)):

    product_data = await get_product_with_text_product_code(session, product_code, lang)
    print(product_data)
    if not product_data:
        return templates.TemplateResponse("product.html", {"request": request, "error": "Product not found"})
    return templates.TemplateResponse("product.html", {"request": request, "product": product_data})
