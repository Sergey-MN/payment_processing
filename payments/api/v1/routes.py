from uuid import UUID

from fastapi import APIRouter, Header, Path, Depends
from starlette.status import HTTP_200_OK, HTTP_202_ACCEPTED

from payments.api.v1.dependencies import get_payments_service
from payments.schemas import PaymentDetail, PaymentCreateResponse, PaymentCreate
from payments.security import verify_api_key
from payments.service import PaymentsService

router_v1 = APIRouter(prefix='/api/v1/payments',
                      tags=['api'],
                      dependencies=[Depends(verify_api_key)]
                      )


@router_v1.post('/', response_model=PaymentCreateResponse, status_code=HTTP_202_ACCEPTED, summary='Создать платеж')
async def create_payment(payment: PaymentCreate, idempotency_key: UUID = Header(),
                         service: PaymentsService = Depends(get_payments_service)):
    obj = await service.create(payment, idempotency_key)
    return PaymentCreateResponse.model_validate(obj)


@router_v1.get('/{payment_id}', response_model=PaymentDetail, status_code=HTTP_200_OK, summary='Получить платеж по id')
async def get_payment(payment_id: int = Path(..., gt=0), service: PaymentsService = Depends(get_payments_service)):
    return await service.get(payment_id)
