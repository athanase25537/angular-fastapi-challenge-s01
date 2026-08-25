from models.database_models import User, UserStatus
from api.user.user_schema import UserCreate, UserUpdate, UserRead
from sqlmodel import Session, select
from uuid import UUID
from passlib.context import CryptContext
from datetime import datetime

# Configuration du contexte de hachage de mot de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    @staticmethod
    def hash_password(password: str) -> str:
        """Hacher un mot de passe"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Vérifier un mot de passe"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_user(user: UserCreate, session: Session) -> UserRead:
        """Créer un nouvel utilisateur"""
        try:
            # Vérifier si l'email existe déjà
            existing_user = session.exec(
                select(User).where(User.email == user.email)
            ).first()
            
            if existing_user:
                raise ValueError(f"Un utilisateur avec l'email {user.email} existe déjà")

            # Vérifier si le numéro de téléphone existe déjà
            existing_phone = session.exec(
                select(User).where(User.phone_number == user.phone_number)
            ).first()
            
            if existing_phone:
                raise ValueError(f"Un utilisateur avec ce numéro de téléphone existe déjà")

            # Créer le nouvel utilisateur
            new_user = User(
                email=user.email,
                phone_number=user.phone_number,
                password_hash=UserService.hash_password(user.password),
                first_name=user.first_name,
                last_name=user.last_name,
                date_of_birth=user.date_of_birth,
                status=UserStatus.PENDING
            )
            
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            
            return UserRead.from_orm(new_user)
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def get_user(user_id: UUID, session: Session) -> UserRead:
        """Récupérer un utilisateur par ID"""
        user = session.exec(
            select(User).where(User.id == user_id)
        ).first()
        
        if not user:
            raise ValueError(f"Utilisateur avec l'ID {user_id} non trouvé")
        
        return UserRead.from_orm(user)

    @staticmethod
    def get_user_by_email(email: str, session: Session) -> UserRead:
        """Récupérer un utilisateur par email"""
        user = session.exec(
            select(User).where(User.email == email)
        ).first()
        
        if not user:
            raise ValueError(f"Utilisateur avec l'email {email} non trouvé")
        
        return UserRead.from_orm(user)

    @staticmethod
    def get_all_users(session: Session, skip: int = 0, limit: int = 100) -> tuple[list[UserRead], int]:
        """Récupérer tous les utilisateurs avec pagination"""
        users = session.exec(
            select(User).offset(skip).limit(limit)
        ).all()
        
        total = session.exec(select(User)).all().__len__()
        
        return [UserRead.from_orm(user) for user in users], total

    @staticmethod
    def update_user(user_id: UUID, user_update: UserUpdate, session: Session) -> UserRead:
        """Mettre à jour un utilisateur"""
        try:
            user = session.exec(
                select(User).where(User.id == user_id)
            ).first()
            
            if not user:
                raise ValueError(f"Utilisateur avec l'ID {user_id} non trouvé")

            # Mettre à jour les champs fournis
            update_data = user_update.dict(exclude_unset=True)
            
            # Vérifier l'unicité de l'email si modifié
            if "email" in update_data and update_data["email"] != user.email:
                existing_email = session.exec(
                    select(User).where(User.email == update_data["email"])
                ).first()
                if existing_email:
                    raise ValueError(f"Un utilisateur avec l'email {update_data['email']} existe déjà")

            # Vérifier l'unicité du numéro de téléphone si modifié
            if "phone_number" in update_data and update_data["phone_number"] != user.phone_number:
                existing_phone = session.exec(
                    select(User).where(User.phone_number == update_data["phone_number"])
                ).first()
                if existing_phone:
                    raise ValueError(f"Un utilisateur avec ce numéro de téléphone existe déjà")

            # Mettre à jour les attributs
            for field, value in update_data.items():
                if value is not None:
                    setattr(user, field, value)
            
            user.updated_at = datetime.utcnow()
            
            session.add(user)
            session.commit()
            session.refresh(user)
            
            return UserRead.from_orm(user)
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def delete_user(user_id: UUID, session: Session) -> dict:
        """Supprimer un utilisateur"""
        try:
            user = session.exec(
                select(User).where(User.id == user_id)
            ).first()
            
            if not user:
                raise ValueError(f"Utilisateur avec l'ID {user_id} non trouvé")
            
            session.delete(user)
            session.commit()
            
            return {"message": f"Utilisateur {user_id} supprimé avec succès"}
        except Exception as e:
            session.rollback()
            raise e