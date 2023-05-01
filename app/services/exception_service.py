from fastapi import HTTPException
from starlette import status

from app.constants.constants import (
    AuthConstants,
    DetailExceptionConstants,
    UserMsgConstants,
)


class ExceptionService:
    class NotFoundException(HTTPException):
        def __init__(self, table_name: str) -> None:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=DetailExceptionConstants.RECORD_NOT_FOUND.replace(
                    "{Record}", table_name
                ),
            )

    class UserCurrentPasswordIncorrect(HTTPException):
        def __init__(self) -> None:
            super().__init__(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=UserMsgConstants.USER_CURRENT_PASSWORD_IS_INCORRECT,
            )

    class UserNotHavePermission(HTTPException):
        def __init__(self):
            super().__init__(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=UserMsgConstants.USER_NOT_HAVE_PERMISSION,
            )

    class InvalidOrExpiredToken(HTTPException):
        def __init__(self):
            super().__init__(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=AuthConstants.INVALID_OR_EXPIRED_TOKEN,
            )

    class InvalidCredential(HTTPException):
        def __init__(self):
            super().__init__(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=AuthConstants.INVALID_CREDENTIAL,
            )
