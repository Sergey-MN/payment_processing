from uuid import UUID as PyUUID

from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from outbox.models import PaymentOutbox
from payments.schemas import PaymentCreate


class OutboxRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def create(self, payment: PaymentCreate, idempotency_key: PyUUID) -> None:
        record = PaymentOutbox(idempotency_key=idempotency_key,
                               payload=payment.model_dump(mode="json", round_trip=True))
        self.session.add(record)

    async def get_new(self, limit: int = 10) -> Sequence[PaymentOutbox]:
        stmt = select(PaymentOutbox).where(PaymentOutbox.sent == False).with_for_update(skip_locked=True).limit(limit)
        records = await self.session.execute(stmt)
        return records.scalars().all()

    async def mark_sent(self, record_id: int) -> None:
        record = await self.session.get(PaymentOutbox, record_id)
        record.sent = True
        await self.session.flush()

