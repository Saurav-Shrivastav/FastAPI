from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.db import users, database
from app.schemas.users import UserDatabaseSchema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(username: str):
    query = users.select().where(username == users.c.username)
    user_obj = await database.fetch_one(query=query)
    return dict(user_obj)


async def validate_user(user: OAuth2PasswordRequestForm = Depends()):
    db_user = await get_user(user.username)
    try:
        db_user = await get_user(user.username)
    except Exception:
        print("here")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not verify_password(user.password, db_user['password']):
        print("no here")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return db_user
