import time
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from app.constants.constants import AuthConstants
from app.constants.routers import ROUTE_TOKEN_URL
from app.models.user import User
from app.services.exception_service import ExceptionService
from app.settings import settings

oa2_bearer = OAuth2PasswordBearer(tokenUrl=ROUTE_TOKEN_URL)


class AuthService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.token_type = AuthConstants.BEARER_TOKEN_TYPE
        self.exception_service = ExceptionService

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def authenticate_user(self, username: str, password: str, db: Session):
        user = db.query(User).filter(User.username == username).first()

        if not user:
            raise self.exception_service.NotFoundException("User")

        if not self.verify_password(password, user.hashed_password):
            raise self.exception_service.InvalidCredential()

        return user

    def _token_response(self, token: str):
        return {"access_token": token, "token_type": self.token_type}

    def create_access_token(self, user: User, expires: Optional[timedelta] = None):
        expires = (
            datetime.utcnow() + expires
            if expires
            else datetime.utcnow()
            + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        claims = {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_admin": user.is_admin,
            "exp": expires,
        }

        token = jwt.encode(
            claims, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )

        return self._token_response(token)

    def _token_interceptor(self, token: str = Depends(oa2_bearer)):
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
            )

            user = User()
            user.id = payload.get("id")
            user.email = payload.get("email")
            user.username = payload.get("username")
            user.first_name = payload.get("first_name")
            user.last_name = payload.get("last_name")
            user.is_admin = payload.get("is_admin")

            exp = payload.get("exp")

            if user.username is None or user.id is None:
                self._token_exception()

            if exp < time.time():
                raise self.exception_service.InvalidOrExpiredToken()

            return user

        except JWTError:
            self._token_exception()

    def _token_exception(self):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credential",
            headers={"WWW-Authenticate": self.token_type},
        )

    def get_token_interceptor(self):
        return Depends(self._token_interceptor)
