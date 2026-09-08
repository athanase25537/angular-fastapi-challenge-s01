from models.database_models import Transaction, TransactionStatus
from api.transaction.transaction_models import TransactionCreate, TransactionUpdate, TransactionRead
from sqlmodel import Session, select
from uuid import UUID
from datetime import datetime
import uuid as uuid_lib


class TransactionService:

    @staticmethod
    def generate_reference() -> str:
        """Générer une référence unique pour la transaction"""
        return f"TRX-{uuid_lib.uuid4().hex[:12].upper()}"

    @staticmethod
    def create_transaction(transaction: TransactionCreate, session: Session) -> TransactionRead:
        """Créer une nouvelle transaction"""
        try:
            # Valider les comptes si fournis
            if transaction.source_account_id and transaction.destination_account_id:
                if transaction.source_account_id == transaction.destination_account_id:
                    raise ValueError("Les comptes source et destination ne peuvent pas être identiques")

            new_transaction = Transaction(
                reference=TransactionService.generate_reference(),
                source_account_id=transaction.source_account_id,
                destination_account_id=transaction.destination_account_id,
                transaction_type=transaction.transaction_type,
                amount=transaction.amount,
                currency_code=transaction.currency_code,
                description=transaction.description,
                status=TransactionStatus.PENDING
            )

            session.add(new_transaction)
            session.commit()
            session.refresh(new_transaction)

            return TransactionRead.model_validate(new_transaction)
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def get_transaction(transaction_id: UUID, session: Session) -> TransactionRead:
        """Récupérer une transaction par ID"""
        transaction = session.exec(
            select(Transaction).where(Transaction.id == transaction_id)
        ).first()

        if not transaction:
            raise ValueError(f"Transaction avec l'ID {transaction_id} non trouvée")

        return TransactionRead.model_validate(transaction)

    @staticmethod
    def get_transaction_by_reference(reference: str, session: Session) -> TransactionRead:
        """Récupérer une transaction par sa référence"""
        transaction = session.exec(
            select(Transaction).where(Transaction.reference == reference)
        ).first()

        if not transaction:
            raise ValueError(f"Transaction avec la référence {reference} non trouvée")

        return TransactionRead.model_validate(transaction)

    @staticmethod
    def get_all_transactions(
        session: Session,
        skip: int = 0,
        limit: int = 100,
        status: TransactionStatus = None,
        transaction_type: str = None
    ) -> tuple[list[TransactionRead], int]:
        """Récupérer toutes les transactions avec filtrage optionnel"""
        query = select(Transaction)

        if status:
            query = query.where(Transaction.status == status)

        if transaction_type:
            query = query.where(Transaction.transaction_type == transaction_type)

        transactions = session.exec(query.offset(skip).limit(limit)).all()

        total = session.exec(query).all().__len__()

        return [TransactionRead.model_validate(t) for t in transactions], total

    @staticmethod
    def get_account_transactions(
        account_id: UUID,
        session: Session,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[list[TransactionRead], int]:
        """Récupérer les transactions d'un compte (entrantes et sortantes)"""
        query = select(Transaction).where(
            (Transaction.source_account_id == account_id) |
            (Transaction.destination_account_id == account_id)
        )

        transactions = session.exec(query.offset(skip).limit(limit)).all()
        total = session.exec(query).all().__len__()

        return [TransactionRead.model_validate(t) for t in transactions], total

    @staticmethod
    def update_transaction(
        transaction_id: UUID,
        transaction_update: TransactionUpdate,
        session: Session
    ) -> TransactionRead:
        """Mettre à jour une transaction"""
        try:
            transaction = session.exec(
                select(Transaction).where(Transaction.id == transaction_id)
            ).first()

            if not transaction:
                raise ValueError(f"Transaction avec l'ID {transaction_id} non trouvée")

            # Mettre à jour les champs fournis
            update_data = transaction_update.dict(exclude_unset=True)

            for field, value in update_data.items():
                if value is not None:
                    setattr(transaction, field, value)

            transaction.updated_at = datetime.utcnow()

            session.add(transaction)
            session.commit()
            session.refresh(transaction)

            return TransactionRead.model_validate(transaction)
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def complete_transaction(transaction_id: UUID, session: Session) -> TransactionRead:
        """Marquer une transaction comme complétée"""
        try:
            transaction = session.exec(
                select(Transaction).where(Transaction.id == transaction_id)
            ).first()

            if not transaction:
                raise ValueError(f"Transaction avec l'ID {transaction_id} non trouvée")

            transaction.status = TransactionStatus.COMPLETED
            transaction.completed_at = datetime.utcnow()
            transaction.updated_at = datetime.utcnow()

            session.add(transaction)
            session.commit()
            session.refresh(transaction)

            return TransactionRead.model_validate(transaction)
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def cancel_transaction(transaction_id: UUID, session: Session) -> TransactionRead:
        """Annuler une transaction"""
        try:
            transaction = session.exec(
                select(Transaction).where(Transaction.id == transaction_id)
            ).first()

            if not transaction:
                raise ValueError(f"Transaction avec l'ID {transaction_id} non trouvée")

            if transaction.status == TransactionStatus.COMPLETED:
                raise ValueError("Impossible d'annuler une transaction complétée")

            transaction.status = TransactionStatus.CANCELLED
            transaction.updated_at = datetime.utcnow()

            session.add(transaction)
            session.commit()
            session.refresh(transaction)

            return TransactionRead.model_validate(transaction)
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def delete_transaction(transaction_id: UUID, session: Session) -> dict:
        """Supprimer une transaction (seulement si elle est en attente)"""
        try:
            transaction = session.exec(
                select(Transaction).where(Transaction.id == transaction_id)
            ).first()

            if not transaction:
                raise ValueError(f"Transaction avec l'ID {transaction_id} non trouvée")

            if transaction.status != TransactionStatus.PENDING:
                raise ValueError("Seules les transactions en attente peuvent être supprimées")

            session.delete(transaction)
            session.commit()

            return {"message": f"Transaction {transaction_id} supprimée avec succès"}
        except Exception as e:
            session.rollback()
            raise e
