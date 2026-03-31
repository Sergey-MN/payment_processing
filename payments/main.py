from fastapi import FastAPI

from payments.api.v1.routes import router_v1
from payments.exceptions import AppError
from payments.handlers import app_error_handler, any_error_handler

app = FastAPI(
    title='Асинхронный сервис процессинга платежей',
)

app.include_router(router_v1)

app.add_exception_handler(AppError, app_error_handler)

app.add_exception_handler(Exception, any_error_handler)
