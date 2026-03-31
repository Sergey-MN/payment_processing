from uuid import UUID as PyUUID

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column

from payments.database import Base


class IdempotencyKey(Base):
    __tablename__ = 'idempotency_keys'

    idempotency_key: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), nullable=False, primary_key=True)
