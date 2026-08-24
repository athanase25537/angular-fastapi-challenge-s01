from models.database_models import User
from api.user.user_schema import UserCreate
from sqlmodel import Session

class UserService:

    def create_user(user: UserCreate, session: Session):
        return {"user": user}