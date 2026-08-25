from fastapi import APIRouter
from api.user.user_routes import router as user_router


router = APIRouter()

router.include_router(router=user_router, prefix="/user", tags=["User"])