from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from outbox.repository import OutboxRepository
from payments.database import get_session
from payments.repository import PaymentsRepository
from payments.service import PaymentsService


def get_payments_service(session: AsyncSession = Depends(get_session)):
    return PaymentsService(PaymentsRepository(session), OutboxRepository(session))
