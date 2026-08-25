from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional
from uuid import UUID
from sqlmodel import Field
from models.database_models import UserStatus


class UserBase(BaseModel):
    email: EmailStr
    phone_number: str = Field(max_length=30)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    date_of_birth: Optional[date] = None


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(default=None, max_length=30)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    date_of_birth: Optional[date] = None


class UserRead(UserBase):
    id: UUID
    status: UserStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    message: str
    data: Optional[UserRead] = None


class UserListResponse(BaseModel):
    message: str
    data: list[UserRead] = []
    count: int = 0