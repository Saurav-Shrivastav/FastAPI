from app.schemas.notifs import NotifInSchema
from app.db import notifs, database

from fastapi import HTTPException
from sqlalchemy import and_


async def create_notif(payload: NotifInSchema):
    query = notifs.insert().values(title=payload.title, description=payload.description, user=payload.user, read_status=False)
    notif_id = await database.execute(query=query)
    return {
        "id": notif_id,
        "title": payload.title,
        "description": payload.description,
        "user": payload.user,
    }


async def get_notif(id: int):
    query = notifs.select().where(id == notifs.c.id)
    return await database.fetch_one(query=query)


async def get_notifs(current_user):
    query = notifs.select().where(and_(current_user["id"] == notifs.c.user, False == notifs.c.read_status))
    return await database.fetch_all(query=query)


async def update_notif(id: int, payload: NotifInSchema):
    query = (
        notifs
        .update()
        .where(id == notifs.c.id)
        .values(title=payload.title, description=payload.description)
        .returning(notifs.c.id)
    )
    return await database.execute(query=query)


async def delete_notif(id: int):
    query = notifs.delete().where(id == notifs.c.id)
    return await database.execute(query=query)


async def read_notif(id: int, current_user):
    query = (
        notifs
        .update()
        .where(id == notifs.c.id)
        .values(read_status=True)
        .returning(notifs.c.id)
    )
    result = await database.execute(query=query)
    return await get_notif(id)
