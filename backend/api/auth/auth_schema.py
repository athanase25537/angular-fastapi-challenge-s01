from pydantic import BaseModel, EmailStr, Field

from api.user.user_schema import UserCreate, UserRead


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


RegisterRequest = UserCreate
