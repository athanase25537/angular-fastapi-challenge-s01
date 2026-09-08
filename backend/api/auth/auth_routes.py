from fastapi import APIRouter, HTTPException
from starlette import status

from api.auth.auth_dependencies import current_user_dependency
from api.auth.auth_schema import LoginRequest, RegisterRequest, TokenResponse
from api.user.user_schema import UserRead
from api.user.user_services import UserService
from core.database import db_dependency
from core.security import create_access_token


router = APIRouter()


def _token_response(user: UserRead) -> TokenResponse:
    return TokenResponse(access_token=create_access_token(str(user.id)), user=user)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
def register(payload: RegisterRequest, session: db_dependency):
    """Create an account and immediately return an access token."""
    try:
        return _token_response(UserService.create_user(payload, session))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, session: db_dependency):
    """Authenticate with email and password."""
    user = UserService.authenticate(payload.email, payload.password, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return _token_response(user)


@router.get("/me", response_model=UserRead)
def me(user: current_user_dependency):
    return UserRead.model_validate(user)
