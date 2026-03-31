from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from consumer.models import IdempotencyKey
from payments.models import Status, Payment


async def update_status(session: AsyncSession, payment_id: int, status: Status) -> None:
    obj = await session.get(Payment, payment_id)
    if not obj:
        raise Exception('Payment not found')
    obj.status = status


async def save_idempotency_key(session: AsyncSession, idempotency_key: UUID) -> bool:
    try:
        obj = IdempotencyKey(idempotency_key=idempotency_key)
        session.add(obj)
        await session.flush()
        return True

    except IntegrityError:
        await session.rollback()
        return False
