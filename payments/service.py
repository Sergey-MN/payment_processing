from uuid import UUID as PyUUID

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from outbox.repository import OutboxRepository
from payments.exceptions import PaymentNotFoundError, DatabaseError, ConflictError
from payments.models import Payment
from payments.repository import PaymentsRepository
from payments.schemas import PaymentCreate


class PaymentsService:
    def __init__(self, repo: PaymentsRepository, outbox: OutboxRepository):
        self.repo = repo
        self.outbox = outbox

    async def create(self, payment: PaymentCreate, idempotency_key: PyUUID) -> Payment:
        pay_data = payment.model_dump()
        pay_data['webhook_url'] = str(pay_data['webhook_url'])
        try:
            obj = await self.repo.create(pay_data, idempotency_key)
            self.outbox.create(payment, idempotency_key)
            await self.repo.session.commit()
            await self.repo.session.refresh(obj)
            return obj

        except IntegrityError as e:
            await self.repo.session.rollback()
            raise ConflictError() from e

        except SQLAlchemyError as e:
            await self.repo.session.rollback()
            raise DatabaseError() from e

    async def get(self, payment_id: int) -> Payment:
        obj = await self.repo.get(payment_id)
        if obj is None:
            raise PaymentNotFoundError()
        return obj
