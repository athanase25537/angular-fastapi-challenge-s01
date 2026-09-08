from fastapi import APIRouter, HTTPException, Query, Path
from api.user.user_services import UserService
from api.user.user_schema import UserCreate, UserUpdate, UserRead, UserResponse, UserListResponse
from starlette import status
from core.database import db_dependency
from uuid import UUID
from api.auth.auth_dependencies import current_user_dependency

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, session: db_dependency):
    """Créer un nouvel utilisateur"""
    try:
        created_user = UserService.create_user(user=user, session=session)
        return {
            "message": "Utilisateur créé avec succès",
            "data": created_user
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/list", response_model=UserListResponse)
def get_all_users(
    session: db_dependency,
    current_user: current_user_dependency,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Récupérer tous les utilisateurs avec pagination"""
    try:
        # There is no administration role flow yet; do not expose every user's
        # personal data to a normal authenticated customer.
        users, total = [UserRead.model_validate(current_user)], 1
        return {
            "message": "Utilisateurs récupérés avec succès",
            "data": users,
            "count": total
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    session: db_dependency,
    current_user: current_user_dependency,
    user_id: UUID = Path(..., description="ID de l'utilisateur"),
):
    """Récupérer un utilisateur par ID"""
    try:
        if current_user.id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        user = UserService.get_user(user_id=user_id, session=session)
        return {
            "message": "Utilisateur récupéré avec succès",
            "data": user
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    session: db_dependency,
    current_user: current_user_dependency,
    user_id: UUID = Path(..., description="ID de l'utilisateur"),
    user_update: UserUpdate = None,
):
    """Mettre à jour un utilisateur"""
    try:
        if current_user.id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        updated_user = UserService.update_user(user_id=user_id, user_update=user_update, session=session)
        return {
            "message": "Utilisateur mis à jour avec succès",
            "data": updated_user
        }
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    session: db_dependency,
    current_user: current_user_dependency,
    user_id: UUID = Path(..., description="ID de l'utilisateur"),
):
    """Supprimer un utilisateur"""
    try:
        if current_user.id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        UserService.delete_user(user_id=user_id, session=session)
        return None
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
