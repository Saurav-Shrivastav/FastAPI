from typing import Optional

from pydantic import BaseModel, Field


class NotifInSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)
    user: int


class NotifOutSchema(NotifInSchema):
    id: int


class UpdateNotif(BaseModel):
    title: Optional[str]
    content: Optional[str]
