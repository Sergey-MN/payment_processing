class AppError(Exception):
    status_code = 500
    detail = "Internal server error"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail


class NotFoundError(AppError):
    status_code = 404
    detail = "Resource not found"


class PaymentNotFoundError(NotFoundError):
    detail = "Payment not found"


class UnauthorizedError(AppError):
    status_code = 401
    detail = "Unauthorized"


class ForbiddenError(AppError):
    status_code = 403
    detail = "Forbidden"


class ConflictError(AppError):
    status_code = 409
    detail = "Conflict"


class DatabaseError(AppError):
    status_code = 500
    detail = "Database error"
