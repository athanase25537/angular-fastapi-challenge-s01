from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID
from decimal import Decimal
from models.database_models import TransactionType, TransactionStatus


class TransactionBase(BaseModel):
    transaction_type: TransactionType
    amount: Decimal = Field(gt=0)
    currency_code: str = Field(max_length=3)
    description: Optional[str] = Field(default=None, max_length=500)


class TransactionCreate(TransactionBase):
    source_account_id: Optional[UUID] = None
    destination_account_id: Optional[UUID] = None


class TransactionUpdate(BaseModel):
    status: Optional[TransactionStatus] = None
    description: Optional[str] = Field(default=None, max_length=500)
    completed_at: Optional[datetime] = None


class TransactionRead(TransactionBase):
    id: UUID
    reference: str
    status: TransactionStatus
    source_account_id: Optional[UUID]
    destination_account_id: Optional[UUID]
    fee: Decimal
    initiated_at: datetime
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TransactionResponse(BaseModel):
    message: str
    data: Optional[TransactionRead] = None


class TransactionListResponse(BaseModel):
    message: str
    data: list[TransactionRead] = []
    count: int = 0
