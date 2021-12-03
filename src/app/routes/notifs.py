from typing import List

from fastapi import APIRouter, Depends, HTTPException

import app.crud.notifs as crud
from app.auth.jwthandler import get_current_user
from app.schemas.notifs import NotifOutSchema, NotifInSchema, UpdateNotif
from app.schemas.token import Status
from app.schemas.users import UserOutSchema


router = APIRouter()


@router.get(
    "/notifs",
    response_model=List[NotifOutSchema],
    dependencies=[Depends(get_current_user)],
)
async def get_notifs(current_user: UserOutSchema = Depends(get_current_user)):
    return await crud.get_notifs(current_user)


@router.get(
    "/notif/{notif_id}",
    response_model=NotifOutSchema,
    dependencies=[Depends(get_current_user)],
)
async def get_notif(notif_id: int, current_user: UserOutSchema = Depends(get_current_user)) -> NotifOutSchema:
    try:
        return await crud.get_notif(notif_id)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="notif does not exist",
        )


@router.post(
    "/notifs", response_model=NotifOutSchema, dependencies=[Depends(get_current_user)]
)
async def create_notif(notif: NotifInSchema) -> NotifOutSchema:
    return await crud.create_notif(notif)


@router.patch(
    "/notif/{notif_id}",
    dependencies=[Depends(get_current_user)],
    response_model=NotifOutSchema,
)
async def update_notif(
    notif_id: int,
    notif: UpdateNotif,
) -> NotifOutSchema:
    return await crud.update_notif(notif_id, notif)


@router.delete(
    "/notif/{notif_id}",
    response_model=Status,
    dependencies=[Depends(get_current_user)],
)
async def delete_notif(notif_id: int):
    return await crud.delete_notif(notif_id)


@router.get(
    "/notif/{notif_id}/read",
    response_model=NotifOutSchema,
    dependencies=[Depends(get_current_user)],
)
async def read_notif(notif_id: int, current_user: UserOutSchema = Depends(get_current_user)):
    return await crud.read_notif(notif_id, current_user)
