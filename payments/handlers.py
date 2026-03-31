import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from payments.exceptions import AppError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def any_error_handler(request: Request, exc: Exception):
    logger.exception(exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
