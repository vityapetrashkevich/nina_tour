from fastapi import APIRouter, Depends, Request, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.utils import md_to_safe_html, ensure_dict, build_image_url
from app.apis.deps import get_session
from app.database.crud.product_files import get_product_file
from app.database.crud.product import get_product_by_code
from app.core.config import Languages
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/thank-you", tags=["Thank You"])
templates = Jinja2Templates(directory="app/web/templates")


@router.get("/{product_code}/{lang}")
async def thank_you_page(
    request: Request,
    product_code: str,
    lang: Languages,
    session: AsyncSession = Depends(get_session)
):
    # 1. Получаем продукт
    product = await get_product_by_code(session, product_code)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # 2. Получаем файл для языка
    file = await get_product_file(session, product.id, lang)

    if not file:
        raise HTTPException(status_code=404, detail="File for this language not found")
    file_norm = ensure_dict(file)

    # Work on a copy for rendering
    render_file = dict(file_norm)
    link = f"/api/v1/download/{render_file['id']}"
    render_file['description_html'] = md_to_safe_html(render_file.get("description").replace("https://example.com>", link))
    render_file['link'] = link

    return templates.TemplateResponse(
        "thank_you.html",
        {
            "request": request,
            "file": render_file,
            "lang": lang,
        }
    )
