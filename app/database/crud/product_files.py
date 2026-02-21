from typing import Optional, List

from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models.product_files import ProductFile
from app.schemas.product_file import (
    ProductFileCreate,
    ProductFileUpdate,
    ProductFileResponse,
)
from app.core.config import Languages


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------
async def create_product_file(
    session: AsyncSession,
    data: ProductFileCreate
) -> ProductFileResponse:

    product_file = ProductFile(
        product_id=data.product_id,
        lang=data.lang.value if isinstance(data.lang, Languages) else data.lang,
        file_link=data.file_link,
        description=data.description,
    )

    session.add(product_file)
    await session.commit()
    await session.refresh(product_file)

    return ProductFileResponse.model_validate(product_file, from_attributes=True)


# ---------------------------------------------------------
# READ
# ---------------------------------------------------------
async def get_product_file_by_id(
    session: AsyncSession,
    file_id: int
) -> Optional[ProductFileResponse]:

    result = await session.execute(
        select(ProductFile).where(ProductFile.id == file_id)
    )
    obj = result.scalar_one_or_none()
    return ProductFileResponse.model_validate(obj, from_attributes=True) if obj else None


async def get_product_file(
    session: AsyncSession,
    product_id: int,
    lang: Languages
) -> Optional[ProductFileResponse]:

    result = await session.execute(
        select(ProductFile)
        .where(ProductFile.product_id == product_id)
        .where(ProductFile.lang == lang.value)
    )
    obj = result.scalar_one_or_none()
    return ProductFileResponse.model_validate(obj, from_attributes=True) if obj else None


async def get_files_for_product(
    session: AsyncSession,
    product_id: int
) -> List[ProductFileResponse]:

    result = await session.execute(
        select(ProductFile).where(ProductFile.product_id == product_id)
    )
    objs = result.scalars().all()
    return [ProductFileResponse.model_validate(o, from_attributes=True) for o in objs]


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------
async def update_product_file(
    session: AsyncSession,
    file_id: int,
    data: ProductFileUpdate
) -> Optional[ProductFileResponse]:

    result = await session.execute(
        select(ProductFile).where(ProductFile.id == file_id)
    )
    product_file = result.scalar_one_or_none()

    if not product_file:
        return None

    update_data = data.model_dump(exclude_unset=True)

    if "lang" in update_data:
        update_data["lang"] = (
            update_data["lang"].value
            if isinstance(update_data["lang"], Languages)
            else update_data["lang"]
        )

    for key, value in update_data.items():
        setattr(product_file, key, value)

    session.add(product_file)
    await session.commit()
    await session.refresh(product_file)

    return ProductFileResponse.model_validate(product_file, from_attributes=True)


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------
async def delete_product_file(
    session: AsyncSession,
    file_id: int
) -> bool:

    result = await session.execute(
        select(ProductFile).where(ProductFile.id == file_id)
    )
    product_file = result.scalar_one_or_none()

    if not product_file:
        return False

    await session.delete(product_file)
    await session.commit()
    return True
