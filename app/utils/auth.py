from functools import wraps

from app.models.user import User
from app.services.exception_service import ExceptionService


def admin_permission_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user: User = kwargs.get("user")

            if not user.is_admin:
                raise ExceptionService.UserNotHavePermission()

            return func(*args, **kwargs)

        return wrapper

    return decorator
