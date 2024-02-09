from datetime import datetime
from typing import Optional, ClassVar

from pydantic import BaseModel, EmailStr, Field
from pydantic_settings import BaseSettings

from src.schemas.user import UserResponse


class TodoSchema(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=250)
    completed: Optional[bool] = False


class TodoUpdateSchema(TodoSchema):
    completed: bool


class TodoResponse(BaseModel):
    id: int = 1
    title: str
    description: str
    completed: bool
    created_at: datetime | None
    updated_at: datetime | None
    user: UserResponse | None

    class Settings(BaseSettings):
        from_attributes: ClassVar[bool] = True
