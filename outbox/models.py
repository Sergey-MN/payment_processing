from uuid import UUID as PyUUID

from sqlalchemy import UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from payments.database import Base


class PaymentOutbox(Base):
    __tablename__ = 'payment_outbox'

    id: Mapped[int] = mapped_column(primary_key=True)
    idempotency_key: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), nullable=False, unique=True)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    sent: Mapped[bool] = mapped_column(default=False, nullable=False)
