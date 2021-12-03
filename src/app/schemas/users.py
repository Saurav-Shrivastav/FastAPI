from pydantic import BaseModel, Field


class UserInSchema(BaseModel):
    username: str = Field(..., min_length=4, max_length=10)
    password: str = Field(..., min_length=8, max_length=50)


class UserOutSchema(BaseModel):
    id: int
    username: str


class UserDatabaseSchema(BaseModel):
    id: int
    username: str
    password: str
