from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select

from core.database import get_db
from core.security import credentials_exception, decode_access_token
from models.database_models import User, UserStatus


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    session: Annotated[Session, Depends(get_db)],
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise credentials_exception()
    payload = decode_access_token(credentials.credentials)
    try:
        user_id = UUID(payload["sub"])
    except ValueError:
        raise credentials_exception()
    user = session.exec(select(User).where(User.id == user_id)).first()
    if user is None or user.status in (UserStatus.BLOCKED, UserStatus.INACTIVE):
        raise credentials_exception()
    return user


current_user_dependency = Annotated[User, Depends(get_current_user)]
