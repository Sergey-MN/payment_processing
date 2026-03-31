from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OutboxSchema(BaseModel):
    id: int
    idempotency_key: UUID
    payload: dict

    model_config = ConfigDict(from_attributes=True)
