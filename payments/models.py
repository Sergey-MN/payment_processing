from datetime import datetime
import uuid
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import Numeric, Enum, String, func, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column, Mapped

from payments.database import Base


class Currency(str, PyEnum):
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'


class Status(str, PyEnum):
    pending = 'pending'
    succeeded = 'succeeded'
    failed = 'failed'


class Payment(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 2, asdecimal=True), nullable=False)
    currency: Mapped[Currency] = mapped_column(Enum(Currency), nullable=False, default=Currency.RUB)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    meta_data: Mapped[dict] = mapped_column(JSONB, nullable=False, default={})
    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False, default=Status.pending)
    idempotency_key: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    webhook_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.timezone('utc', func.now()), nullable=False)
    processing_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), default=None, nullable=True)

    def __repr__(self):
        return f'<Payment {self.id}>'
