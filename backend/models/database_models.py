from __future__ import annotations

from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


# ============================================================
# BASE
# ============================================================

class TimestampMixin(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )


# ============================================================
# ENUMS
# ============================================================

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
    PENDING = "pending"


class AccountStatus(str, Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"
    FROZEN = "frozen"
    CLOSED = "closed"
    PENDING = "pending"


class AccountType(str, Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    BUSINESS = "business"
    JOINT = "joint"


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    PAYMENT = "payment"
    CARD_PAYMENT = "card_payment"
    FEE = "fee"
    INTEREST = "interest"
    REFUND = "refund"


class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REVERSED = "reversed"


class CardType(str, Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class CardStatus(str, Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class LoanStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    PAID = "paid"
    DEFAULTED = "defaulted"
    CANCELLED = "cancelled"


class KYCStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"


class DocumentType(str, Enum):
    NATIONAL_ID = "national_id"
    PASSPORT = "passport"
    DRIVER_LICENSE = "driver_license"
    PROOF_OF_ADDRESS = "proof_of_address"
    OTHER = "other"


class NotificationType(str, Enum):
    TRANSACTION = "transaction"
    SECURITY = "security"
    SYSTEM = "system"
    PROMOTION = "promotion"


# ============================================================
# ROLE
# ============================================================

class Role(TimestampMixin, table=True):
    __tablename__ = "roles"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    name: str = Field(
        max_length=50,
        unique=True,
        index=True
    )

    description: Optional[str] = None

    users: list["User"] = Relationship(
        back_populates="role"
    )


# ============================================================
# USER
# ============================================================

class User(TimestampMixin, table=True):
    __tablename__ = "users"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    email: str = Field(
        max_length=255,
        unique=True,
        index=True
    )

    phone_number: str = Field(
        max_length=30,
        unique=True,
        index=True
    )

    password_hash: str = Field(
        max_length=255
    )

    first_name: str = Field(
        max_length=100
    )

    last_name: str = Field(
        max_length=100
    )

    date_of_birth: Optional[date] = None

    status: UserStatus = Field(
        default=UserStatus.PENDING,
        index=True
    )

    role_id: Optional[UUID] = Field(
        default=None,
        foreign_key="roles.id"
    )

    role: Optional["Role"] = Relationship(
        back_populates="users"
    )

    customer_profile: Optional["CustomerProfile"] = Relationship(
        back_populates="user"
    )

    accounts: list["BankAccount"] = Relationship(
        back_populates="owner"
    )

    beneficiaries: list["Beneficiary"] = Relationship(
        back_populates="user"
    )

    loans: list["Loan"] = Relationship(
        back_populates="borrower"
    )

    notifications: list["Notification"] = Relationship(
        back_populates="user"
    )

    documents: list["Document"] = Relationship(
        back_populates="user"
    )

    audit_logs: list["AuditLog"] = Relationship(
        back_populates="user"
    )


# ============================================================
# CUSTOMER PROFILE
# ============================================================

class CustomerProfile(TimestampMixin, table=True):
    __tablename__ = "customer_profiles"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    user_id: UUID = Field(
        foreign_key="users.id",
        unique=True,
        index=True
    )

    customer_number: str = Field(
        max_length=50,
        unique=True,
        index=True
    )

    nationality: Optional[str] = Field(
        default=None,
        max_length=100
    )

    occupation: Optional[str] = Field(
        default=None,
        max_length=150
    )

    user: "User" = Relationship(
        back_populates="customer_profile"
    )

    addresses: list["Address"] = Relationship(
        back_populates="customer"
    )

    kyc_verifications: list["KYCVerification"] = Relationship(
        back_populates="customer"
    )


# ============================================================
# ADDRESS
# ============================================================

class Address(TimestampMixin, table=True):
    __tablename__ = "addresses"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    customer_id: UUID = Field(
        foreign_key="customer_profiles.id",
        index=True
    )

    address_line: str = Field(
        max_length=255
    )

    city: str = Field(
        max_length=100
    )

    region: Optional[str] = Field(
        default=None,
        max_length=100
    )

    postal_code: Optional[str] = Field(
        default=None,
        max_length=30
    )

    country: str = Field(
        max_length=100
    )

    is_primary: bool = Field(
        default=False
    )

    customer: "CustomerProfile" = Relationship(
        back_populates="addresses"
    )


# ============================================================
# CURRENCY
# ============================================================

class Currency(TimestampMixin, table=True):
    __tablename__ = "currencies"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    code: str = Field(
        max_length=3,
        unique=True,
        index=True
    )

    name: str = Field(
        max_length=100
    )

    symbol: Optional[str] = Field(
        default=None,
        max_length=10
    )

    is_active: bool = Field(
        default=True
    )

    accounts: list["BankAccount"] = Relationship(
        back_populates="currency"
    )


# ============================================================
# BANK BRANCH
# ============================================================

class BankBranch(TimestampMixin, table=True):
    __tablename__ = "bank_branches"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    code: str = Field(
        max_length=30,
        unique=True,
        index=True
    )

    name: str = Field(
        max_length=150
    )

    address: Optional[str] = Field(
        default=None,
        max_length=255
    )

    city: Optional[str] = Field(
        default=None,
        max_length=100
    )

    phone_number: Optional[str] = Field(
        default=None,
        max_length=30
    )

    is_active: bool = Field(
        default=True
    )

    accounts: list["BankAccount"] = Relationship(
        back_populates="branch"
    )


# ============================================================
# BANK ACCOUNT
# ============================================================

class BankAccount(TimestampMixin, table=True):
    __tablename__ = "bank_accounts"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    account_number: str = Field(
        max_length=34,
        unique=True,
        index=True
    )

    owner_id: UUID = Field(
        foreign_key="users.id",
        index=True
    )

    branch_id: Optional[UUID] = Field(
        default=None,
        foreign_key="bank_branches.id"
    )

    currency_id: UUID = Field(
        foreign_key="currencies.id"
    )

    account_type: AccountType = Field(
        default=AccountType.CHECKING,
        index=True
    )

    status: AccountStatus = Field(
        default=AccountStatus.PENDING,
        index=True
    )

    balance: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=18,
        decimal_places=2
    )

    available_balance: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=18,
        decimal_places=2
    )

    opened_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    closed_at: Optional[datetime] = None

    owner: "User" = Relationship(
        back_populates="accounts"
    )

    branch: Optional["BankBranch"] = Relationship(
        back_populates="accounts"
    )

    currency: "Currency" = Relationship(
        back_populates="accounts"
    )

    outgoing_transactions: list["Transaction"] = Relationship(
        back_populates="source_account",
        sa_relationship_kwargs={
            "foreign_keys": "[Transaction.source_account_id]"
        }
    )

    incoming_transactions: list["Transaction"] = Relationship(
        back_populates="destination_account",
        sa_relationship_kwargs={
            "foreign_keys": "[Transaction.destination_account_id]"
        }
    )

    ledger_entries: list["LedgerEntry"] = Relationship(
        back_populates="account"
    )

    cards: list["Card"] = Relationship(
        back_populates="account"
    )


# ============================================================
# TRANSACTION
# ============================================================

class Transaction(TimestampMixin, table=True):
    __tablename__ = "transactions"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    reference: str = Field(
        max_length=100,
        unique=True,
        index=True
    )

    source_account_id: Optional[UUID] = Field(
        default=None,
        foreign_key="bank_accounts.id",
        index=True
    )

    destination_account_id: Optional[UUID] = Field(
        default=None,
        foreign_key="bank_accounts.id",
        index=True
    )

    transaction_type: TransactionType = Field(
        index=True
    )

    status: TransactionStatus = Field(
        default=TransactionStatus.PENDING,
        index=True
    )

    amount: Decimal = Field(
        max_digits=18,
        decimal_places=2
    )

    fee: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=18,
        decimal_places=2
    )

    currency_code: str = Field(
        max_length=3
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500
    )

    initiated_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    completed_at: Optional[datetime] = None

    source_account: Optional["BankAccount"] = Relationship(
        back_populates="outgoing_transactions",
        sa_relationship_kwargs={
            "foreign_keys": "[Transaction.source_account_id]"
        }
    )

    destination_account: Optional["BankAccount"] = Relationship(
        back_populates="incoming_transactions",
        sa_relationship_kwargs={
            "foreign_keys": "[Transaction.destination_account_id]"
        }
    )

    ledger_entries: list["LedgerEntry"] = Relationship(
        back_populates="transaction"
    )


# ============================================================
# LEDGER ENTRY
# ============================================================

class LedgerEntry(TimestampMixin, table=True):
    __tablename__ = "ledger_entries"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    transaction_id: UUID = Field(
        foreign_key="transactions.id",
        index=True
    )

    account_id: UUID = Field(
        foreign_key="bank_accounts.id",
        index=True
    )

    amount: Decimal = Field(
        max_digits=18,
        decimal_places=2
    )

    entry_type: str = Field(
        max_length=20
    )

    balance_after: Decimal = Field(
        max_digits=18,
        decimal_places=2
    )

    transaction: "Transaction" = Relationship(
        back_populates="ledger_entries"
    )

    account: "BankAccount" = Relationship(
        back_populates="ledger_entries"
    )


# ============================================================
# BENEFICIARY
# ============================================================

class Beneficiary(TimestampMixin, table=True):
    __tablename__ = "beneficiaries"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    user_id: UUID = Field(
        foreign_key="users.id",
        index=True
    )

    name: str = Field(
        max_length=150
    )

    account_number: str = Field(
        max_length=34,
        index=True
    )

    bank_name: Optional[str] = Field(
        default=None,
        max_length=150
    )

    nickname: Optional[str] = Field(
        default=None,
        max_length=100
    )

    is_active: bool = Field(
        default=True
    )

    user: "User" = Relationship(
        back_populates="beneficiaries"
    )


# ============================================================
# CARD
# ============================================================

class Card(TimestampMixin, table=True):
    __tablename__ = "cards"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    account_id: UUID = Field(
        foreign_key="bank_accounts.id",
        index=True
    )

    card_type: CardType = Field(
        default=CardType.DEBIT
    )

    status: CardStatus = Field(
        default=CardStatus.ACTIVE,
        index=True
    )

    last_four_digits: str = Field(
        max_length=4
    )

    card_number_hash: Optional[str] = Field(
        default=None,
        max_length=255
    )

    expiry_date: date

    issued_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    blocked_at: Optional[datetime] = None

    account: "BankAccount" = Relationship(
        back_populates="cards"
    )


# ============================================================
# LOAN
# ============================================================

class Loan(TimestampMixin, table=True):
    __tablename__ = "loans"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    borrower_id: UUID = Field(
        foreign_key="users.id",
        index=True
    )

    loan_number: str = Field(
        max_length=50,
        unique=True,
        index=True
    )

    principal_amount: Decimal = Field(
        max_digits=18,
        decimal_places=2
    )

    interest_rate: Decimal = Field(
        max_digits=8,
        decimal_places=4
    )

    total_amount: Decimal = Field(
        max_digits=18,
        decimal_places=2
    )

    remaining_amount: Decimal = Field(
        max_digits=18,
        decimal_places=2
    )

    duration_months: int

    status: LoanStatus = Field(
        default=LoanStatus.PENDING,
        index=True
    )

    start_date: Optional[date] = None

    end_date: Optional[date] = None

    borrower: "User" = Relationship(
        back_populates="loans"
    )

    payments: list["LoanPayment"] = Relationship(
        back_populates="loan"
    )


# ============================================================
# LOAN PAYMENT
# ============================================================

class LoanPayment(TimestampMixin, table=True):
    __tablename__ = "loan_payments"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    loan_id: UUID = Field(
        foreign_key="loans.id",
        index=True
    )

    amount: Decimal = Field(
        max_digits=18,
        decimal_places=2
    )

    principal_amount: Decimal = Field(
        max_digits=18,
        decimal_places=2
    )

    interest_amount: Decimal = Field(
        max_digits=18,
        decimal_places=2
    )

    payment_date: datetime = Field(
        default_factory=datetime.utcnow
    )

    loan: "Loan" = Relationship(
        back_populates="payments"
    )


# ============================================================
# KYC
# ============================================================

class KYCVerification(TimestampMixin, table=True):
    __tablename__ = "kyc_verifications"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    customer_id: UUID = Field(
        foreign_key="customer_profiles.id",
        index=True
    )

    status: KYCStatus = Field(
        default=KYCStatus.PENDING,
        index=True
    )

    verified_at: Optional[datetime] = None

    rejection_reason: Optional[str] = Field(
        default=None,
        max_length=500
    )

    customer: "CustomerProfile" = Relationship(
        back_populates="kyc_verifications"
    )


# ============================================================
# DOCUMENT
# ============================================================

class Document(TimestampMixin, table=True):
    __tablename__ = "documents"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    user_id: UUID = Field(
        foreign_key="users.id",
        index=True
    )

    document_type: DocumentType = Field(
        index=True
    )

    file_name: str = Field(
        max_length=255
    )

    file_path: str = Field(
        max_length=500
    )

    mime_type: Optional[str] = Field(
        default=None,
        max_length=100
    )

    verified: bool = Field(
        default=False
    )

    user: "User" = Relationship(
        back_populates="documents"
    )


# ============================================================
# NOTIFICATION
# ============================================================

class Notification(TimestampMixin, table=True):
    __tablename__ = "notifications"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    user_id: UUID = Field(
        foreign_key="users.id",
        index=True
    )

    notification_type: NotificationType = Field(
        index=True
    )

    title: str = Field(
        max_length=200
    )

    message: str = Field(
        max_length=1000
    )

    is_read: bool = Field(
        default=False,
        index=True
    )

    read_at: Optional[datetime] = None

    user: "User" = Relationship(
        back_populates="notifications"
    )


# ============================================================
# AUDIT LOG
# ============================================================

class AuditLog(TimestampMixin, table=True):
    __tablename__ = "audit_logs"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    user_id: Optional[UUID] = Field(
        default=None,
        foreign_key="users.id",
        index=True
    )

    action: str = Field(
        max_length=100,
        index=True
    )

    entity_type: str = Field(
        max_length=100
    )

    entity_id: Optional[str] = Field(
        default=None,
        max_length=100
    )

    ip_address: Optional[str] = Field(
        default=None,
        max_length=45
    )

    user_agent: Optional[str] = Field(
        default=None,
        max_length=500
    )

    details: Optional[str] = None

    user: Optional["User"] = Relationship(
        back_populates="audit_logs"
    )