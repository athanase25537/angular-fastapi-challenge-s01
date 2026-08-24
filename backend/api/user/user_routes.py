from fastapi import APIRouter
from api.user.user_services import UserService
from api.user.user_schema import UserCreate
from starlette import status
from core.database import db_dependency

router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    try:
        UserService.create_user(user=user, session=db_dependency)
    except Exception  as e:
        return { "error": str(e) }
