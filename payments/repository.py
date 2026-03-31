from uuid import UUID as PyUUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from payments.exceptions import DatabaseError
from payments.models import Payment
from payments.schemas import PaymentCreate


class PaymentsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payment: dict, idempotency_key: PyUUID) -> Payment:
        obj = Payment(**payment, idempotency_key=idempotency_key)
        self.session.add(obj)
        return obj

    async def get(self, payment_id: int) -> Payment | None:
        try:
            obj = await self.session.get(Payment, payment_id)
            return obj
        except SQLAlchemyError as e:
            raise DatabaseError() from e
