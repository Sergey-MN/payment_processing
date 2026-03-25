from fastapi import APIRouter, status, Header, Path

from payments.schemas import PaymentDetail, PaymentCreateResponse, PaymentCreate

router = APIRouter(prefix='/api/v1/payments',
                   tags=['api'],
                   )


@router.post('/', response_model=PaymentCreateResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_payment(payment: PaymentCreate, idempotency_key: str = Header()):
    ...


@router.get('/{payment_id}', response_model=PaymentDetail, status_code=status.HTTP_200_OK)
async def get_payment(payment_id: int = Path(..., gt=0)):
    ...
