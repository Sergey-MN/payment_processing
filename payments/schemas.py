from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, HttpUrl

from payments.models import Currency, Status


class PaymentCreate(BaseModel):
    amount: Decimal
    currency: Currency
    description: str
    meta_data: dict
    webhook_url: HttpUrl


class PaymentCreateResponse(BaseModel):
    id: int
    status: Status
    created_at: datetime
    processing_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class PaymentDetail(PaymentCreate, PaymentCreateResponse):
    ...
