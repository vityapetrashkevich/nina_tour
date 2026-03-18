from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from fastapi.security import OAuth2PasswordRequestForm
import httpx
import json
import logging

from app.core.config import settings
from app.apis.deps import get_session, get_current_admin
from app.schemas import AdminRegisterResponse, AdminRegisterRequest, StepUpRequest, StepUpResponse
from app.database.crud.product import get_product_by_ids
from app.database.crud.admin import *
from app.core.security import verify_password, create_access_token

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin")


@router.post("/create", response_model=AdminRegisterResponse)
async def register_new_admin(
        data: AdminRegisterRequest,
        session: AsyncSession = Depends(get_session),
        admin=Depends(get_current_admin)
):
    admin, generated_password = await AdminCRUD.create(session, data)

    return AdminRegisterResponse(
        id=admin.id,
        email=admin.email,
        generated_password=generated_password,
    )


@router.post("/auth/login_json", response_model=StepUpResponse)
async def login_json(
        data: StepUpRequest,
        session: AsyncSession = Depends(get_session),
):
    admin = await AdminCRUD.get_by_email(session, data.email)
    print(str(admin))

    if not admin or not verify_password(data.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(admin.id)

    return StepUpResponse(
        id=admin.id,
        created_at=admin.created_at,
        updated_at=admin.updated_at,
        access_token=token,
    )


@router.post("/auth/login", response_model=StepUpResponse)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session),
):
    admin = await AdminCRUD.get_by_email(session, form_data.username)

    if not admin or not verify_password(form_data.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(admin.id)

    return StepUpResponse(
        id=admin.id,
        created_at=admin.created_at,
        updated_at=admin.updated_at,
        access_token=token,
    )
