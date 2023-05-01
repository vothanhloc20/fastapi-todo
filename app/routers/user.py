from typing import Dict, Type
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from starlette import status

from app.constants.constants import RouteTagConstants, UserMsgConstants
from app.constants.routers import (
    ROUTE_CHANGE_PASSWORD_BY_USER_ID,
    ROUTE_CREATE,
    ROUTE_DELETE_BY_ID,
    ROUTE_GET_BY_ID,
    ROUTE_UPDATE_BY_ID,
    ROUTE_USER,
)
from app.dependencies.user import get_users_filters
from app.models.user import User
from app.schemas.user import (
    UserChangePassword,
    UserCreate,
    UserFilters,
    UserUpdateInformation,
    UserView,
)
from app.services.database_service import DatabaseService
from app.services.user_service import UserService

router = APIRouter(prefix=ROUTE_USER, tags=[RouteTagConstants.USER_TAG])
database_service = DatabaseService()
user_service = UserService()
session = database_service.get_session()


@router.get("", response_model=Page[UserView])
def get_all_users(
    user_filters: UserFilters = Depends(get_users_filters), db: Session = session
) -> Page[UserView]:
    result = user_service.get_all_users(user_filters, db)
    return result


@router.get(ROUTE_GET_BY_ID, response_model=UserView)
def get_user_by_id(uuid: UUID, db: Session = session) -> Type[User] | None:
    result = user_service.get_user_by_id(uuid, db)
    return result


@router.post(ROUTE_CREATE, response_model=UserView, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = session) -> UserView:
    result = user_service.create_new_user(user, db)
    return result


@router.put(ROUTE_UPDATE_BY_ID, response_model=UserView)
def update_information_user_by_user_id(
    user_request: UserUpdateInformation, uuid: UUID, db: Session = session
) -> UserView:
    result = user_service.update_information_user_by_user_id(user_request, uuid, db)
    return result


@router.put(ROUTE_CHANGE_PASSWORD_BY_USER_ID)
def change_password_by_user_id(
    user_request: UserChangePassword, uuid: UUID, db: Session = session
) -> Dict[str, str]:
    user_service.change_password_by_user_id(user_request, uuid, db)
    return {"detail": UserMsgConstants.USER_CHANGE_PASSWORD_SUCCESSFULLY}


@router.delete(ROUTE_DELETE_BY_ID, status_code=status.HTTP_204_NO_CONTENT)
def delete_user(uuid: UUID, db: Session = session) -> None:
    user_service.delete_user(uuid, db)
