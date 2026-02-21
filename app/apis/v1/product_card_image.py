# app/apis/v1/product_card_images.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlmodel.ext.asyncio.session import AsyncSession

from app.apis.deps import get_session
from app.schemas import (
    ProductCardImageCreate,
    ProductCardImageUpdate,
    ProductCardImageResponse,
)
from app.database.crud.product_cards_images import create_product_card_image,  get_product_card_image_by_id
from app.database.crud.product_cards_images import  list_product_card_images, update_product_card_image, delete_product_card_image

router = APIRouter(prefix="/product_card_images")


# -----------------------------
# CREATE
# -----------------------------
@router.post(
    "",
    response_model=ProductCardImageResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_product_card_image_endpoint(
    image_in: ProductCardImageCreate,
    session: AsyncSession = Depends(get_session)
):
    try:
        return await create_product_card_image(session, image_in)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


# -----------------------------
# READ BY ID
# -----------------------------
@router.get(
    "/{image_id}",
    response_model=ProductCardImageResponse
)
async def get_product_card_image_endpoint(
    image_id: int,
    session: AsyncSession = Depends(get_session)
):
    image = await get_product_card_image_by_id(session, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="ProductCardImage not found")
    return image


# -----------------------------
# LIST
# -----------------------------
@router.get(
    "",
    response_model=List[ProductCardImageResponse]
)
async def list_product_card_images_endpoint(
    product_card_id: int | None = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session)
):
    return await list_product_card_images(
        session,
        product_card_id=product_card_id,
        limit=limit,
        offset=offset
    )


# -----------------------------
# UPDATE (PATCH)
# -----------------------------
@router.patch(
    "/{image_id}",
    response_model=ProductCardImageResponse
)
async def update_product_card_image_endpoint(
    image_id: int,
    image_in: ProductCardImageUpdate,
    session: AsyncSession = Depends(get_session)
):
    try:
        updated = await update_product_card_image(session, image_id, image_in)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

    if updated is None:
        raise HTTPException(status_code=404, detail="ProductCardImage not found")

    return updated


# -----------------------------
# DELETE
# -----------------------------
@router.delete(
    "/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product_card_image_endpoint(
    image_id: int,
    session: AsyncSession = Depends(get_session)
):
    deleted = await delete_product_card_image(session, image_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="ProductCardImage not found")
    return None
