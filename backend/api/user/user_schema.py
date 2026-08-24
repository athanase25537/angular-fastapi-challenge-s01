from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from sqlmodel import Field

class UserBase(BaseModel):
    
    email: EmailStr
    phone_number: str = Field(
        max_length=30,
        unique=True,
        index=True
    )
    password: str
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    
class UserCreate(UserBase):
    pass