from fastapi import HTTPException
from passlib.context import CryptContext

from app.schemas.users import UserOutSchema
from app.schemas.token import Status
from app.db import users, database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(user) -> UserOutSchema:
    user.password = pwd_context.encrypt(user.password)

    try:
        query = users.insert().values(username=user.username, password=user.password)
        user_id = await database.execute(query=query)
    except Exception:
        raise HTTPException(status_code=401, detail=f"Sorry, that username already exists.")

    response_obj = {
        "id": user_id,
        "username": user.username
    }
    return response_obj


async def delete_user(user_id, current_user) -> Status:
    try:
        query = users.select().where(user_id == users.c.id)
        db_user_id = await database.execute(query=query)
    except Exception:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    if db_user_id == current_user['id']:
        query = users.delete().where(user_id == users.c.id)
        deleted_count = await database.execute(query=query)
        print("here")
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return Status(message=f"Deleted user {user_id}")

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")
