from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from payments.models import Currency, Status


class PaymentCreate(BaseModel):
    amount: Decimal
    currency: Currency
    description: str
    meta_data: dict
    webhook_url: str


class PaymentCreateResponse(BaseModel):
    id: int
    status: Status
    created_at: datetime


class PaymentDetail(PaymentCreate, PaymentCreateResponse):
    ...
