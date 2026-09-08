from fastapi import APIRouter
from api.user.user_routes import router as user_router
from api.auth.auth_routes import router as auth_router
from api.transaction.transaction_routes import router as transaction_router


router = APIRouter()

router.include_router(router=user_router, prefix="/user", tags=["User"])
router.include_router(router=auth_router, prefix="/auth", tags=["Auth"])
router.include_router(router=transaction_router, prefix="/transactions", tags=["Transactions"])
