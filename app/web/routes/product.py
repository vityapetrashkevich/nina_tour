

from fastapi import APIRouter, Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.templating import Jinja2Templates
import logging

from app.core.utils import md_to_safe_html, ensure_dict, build_image_url
from app.apis.deps import get_session
from app.database.crud.product_with_cards import get_product_with_card_by_code


router = APIRouter(prefix="/products")
templates = Jinja2Templates(directory="app/web/templates")

logger = logging.getLogger("app.web.routes.product")




@router.get("/{lang}/{product_code}")
async def product_page(request: Request, product_code: str, lang: str = "en",
                       session: AsyncSession = Depends(get_session)):
    """
    Render product page. Convert Markdown fields to sanitized HTML and ensure image URLs are public.
    """
    product_data = await get_product_with_card_by_code(session, product_code, lang)
    if not product_data:
        return templates.TemplateResponse("error.html", {"request": request, "lang": lang})


    # Normalize to plain dict
    product = ensure_dict(product_data)

    # Work on a copy for rendering
    render_product = dict(product)

    # Convert top-level description
    render_product["description_html"] = md_to_safe_html(render_product.get("description", "") or "")
    render_product["name_html"] = md_to_safe_html(render_product.get("name", "") or "")
    # Ensure product_code exists for JS pay()
    if not render_product.get("product_code"):
        render_product["product_code"] = product_code

    images = render_product.get("images") or []
    new_images = []

    for img in images:
        i = ensure_dict(img)

        # Markdown → safe HTML
        i["description_html"] = md_to_safe_html(i.get("description", "") or "")

        # Build public URL
        built = build_image_url(request, i)
        i["url"] = built or i.get("url", "")

        # Compose final HTML block (как на скриншоте)
        i["html"] = f"""
        <div class="image-text-block">
            <div class="image-side">
                <img src="{i['url']}" alt="">
            </div>

            <div class="divider"></div>

            <div class="text-side">
                <h2 class="image-title">{i.get('title', '')}</h2>
                <div class="image-description">
                    {i['description_html']}
                </div>
            </div>
        </div>
        """

        new_images.append(i)

    render_product["images"] = new_images

    # Debug logging (can be removed)
    logger.debug("Rendering product page for %s (lang=%s). Keys: %s", product_code, lang, list(render_product.keys()))

    return templates.TemplateResponse("product.html", {"request": request, "product": render_product, "lang": lang})
