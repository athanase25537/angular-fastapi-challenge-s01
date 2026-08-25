from fastapi import APIRouter, HTTPException, Query, Path
from api.transaction.transaction_services import TransactionService
from api.transaction.transaction_models import (
    TransactionCreate,
    TransactionUpdate,
    TransactionRead,
    TransactionResponse,
    TransactionListResponse
)
from models.database_models import TransactionStatus, TransactionType
from starlette import status
from core.database import db_dependency
from uuid import UUID

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, session: db_dependency):
    """Créer une nouvelle transaction"""
    try:
        created_transaction = TransactionService.create_transaction(transaction=transaction, session=session)
        return {
            "message": "Transaction créée avec succès",
            "data": created_transaction
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/list", response_model=TransactionListResponse)
def get_all_transactions(
    session: db_dependency,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: TransactionStatus = Query(None),
    transaction_type: str = Query(None)
):
    """Récupérer toutes les transactions avec filtrage optionnel"""
    try:
        transactions, total = TransactionService.get_all_transactions(
            session=session,
            skip=skip,
            limit=limit,
            status=status,
            transaction_type=transaction_type
        )
        return {
            "message": "Transactions récupérées avec succès",
            "data": transactions,
            "count": total
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: UUID = Path(..., description="ID de la transaction"),
    session: db_dependency = None
):
    """Récupérer une transaction par ID"""
    try:
        transaction = TransactionService.get_transaction(transaction_id=transaction_id, session=session)
        return {
            "message": "Transaction récupérée avec succès",
            "data": transaction
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/reference/{reference}", response_model=TransactionResponse)
def get_transaction_by_reference(
    reference: str = Path(..., description="Référence de la transaction"),
    session: db_dependency = None
):
    """Récupérer une transaction par sa référence"""
    try:
        transaction = TransactionService.get_transaction_by_reference(reference=reference, session=session)
        return {
            "message": "Transaction récupérée avec succès",
            "data": transaction
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/account/{account_id}", response_model=TransactionListResponse)
def get_account_transactions(
    account_id: UUID = Path(..., description="ID du compte"),
    session: db_dependency = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Récupérer les transactions d'un compte"""
    try:
        transactions, total = TransactionService.get_account_transactions(
            account_id=account_id,
            session=session,
            skip=skip,
            limit=limit
        )
        return {
            "message": "Transactions du compte récupérées avec succès",
            "data": transactions,
            "count": total
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: UUID = Path(..., description="ID de la transaction"),
    transaction_update: TransactionUpdate = None,
    session: db_dependency = None
):
    """Mettre à jour une transaction"""
    try:
        updated_transaction = TransactionService.update_transaction(
            transaction_id=transaction_id,
            transaction_update=transaction_update,
            session=session
        )
        return {
            "message": "Transaction mise à jour avec succès",
            "data": updated_transaction
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{transaction_id}/complete", response_model=TransactionResponse)
def complete_transaction(
    transaction_id: UUID = Path(..., description="ID de la transaction"),
    session: db_dependency = None
):
    """Marquer une transaction comme complétée"""
    try:
        completed_transaction = TransactionService.complete_transaction(
            transaction_id=transaction_id,
            session=session
        )
        return {
            "message": "Transaction marquée comme complétée",
            "data": completed_transaction
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{transaction_id}/cancel", response_model=TransactionResponse)
def cancel_transaction(
    transaction_id: UUID = Path(..., description="ID de la transaction"),
    session: db_dependency = None
):
    """Annuler une transaction"""
    try:
        cancelled_transaction = TransactionService.cancel_transaction(
            transaction_id=transaction_id,
            session=session
        )
        return {
            "message": "Transaction annulée avec succès",
            "data": cancelled_transaction
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: UUID = Path(..., description="ID de la transaction"),
    session: db_dependency = None
):
    """Supprimer une transaction (seulement si elle est en attente)"""
    try:
        TransactionService.delete_transaction(transaction_id=transaction_id, session=session)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
