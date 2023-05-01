from typing import Optional, Type
from uuid import UUID

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import and_, select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.elements import BooleanClauseList

from app.models.company import Company
from app.models.user import User
from app.schemas.user import (
    UserChangePassword,
    UserCreate,
    UserFilters,
    UserUpdateInformation,
    UserView,
)
from app.services.auth_service import AuthService
from app.services.database_service import DatabaseService
from app.services.exception_service import ExceptionService


class UserService:
    def __init__(self):
        self.user_model = User
        self.company_model = Company
        self.auth_service = AuthService()
        self.exception_service = ExceptionService()
        self.database_service = DatabaseService(self.user_model)
        self.user_model_name = self.user_model.__name__

    def _filter_user(
        self,
        is_admin: Optional[str] = None,
        is_active: Optional[str] = None,
        company_id: Optional[str] = None,
    ) -> BooleanClauseList:
        domains = []

        if is_admin is not None:
            domains.append(self.user_model.is_admin == is_admin)

        if is_active is not None:
            domains.append(self.user_model.is_active == is_active)

        if company_id:
            domains.append(self.user_model.company_id.in_([company_id]))

        return and_(*domains)

    def get_all_users(self, user_filters: UserFilters, db: Session) -> Page[UserView]:
        domains = self._filter_user(
            is_admin=user_filters.is_admin,
            is_active=user_filters.is_active,
            company_id=user_filters.company_id,
        )

        query = select(self.user_model).options(joinedload(self.user_model.company))

        if not isinstance(domains, BooleanClauseList):
            query = query.filter(domains)

        return paginate(db, query)

    def get_user_by_id(self, uuid: UUID, db: Session) -> Type[User] | None:
        user = (
            db.query(self.user_model)
            .options(joinedload(self.user_model.company))
            .filter(self.user_model.id == uuid)
            .first()
        )

        if not user:
            raise self.exception_service.NotFoundException(self.user_model_name)

        return user

    def create_new_user(self, user: UserCreate, db: Session) -> UserView | None:
        hashed_password = self.auth_service.get_password_hash(user.password)
        new_user = self.user_model(
            **user.dict(exclude={"password", "re_password"}),
            hashed_password=hashed_password
        )
        new_user.save(db)

        return new_user

    def update_information_user_by_user_id(
        self, user_request: UserUpdateInformation, uuid: UUID, db: Session
    ) -> UserView | None:
        user = self.database_service.get_record_by_id(uuid, db)

        for key, value in user_request.dict(exclude_unset=True).items():
            setattr(user, key, value)

        user.save(db)

        return user

    def change_password_by_user_id(
        self, user_request: UserChangePassword, uuid: UUID, db: Session
    ) -> None:
        user = self.database_service.get_record_by_id(uuid, db)

        is_current_password = self.auth_service.verify_password(
            user_request.current_password, user.hashed_password
        )

        if not is_current_password:
            self.exception_service.UserCurrentPasswordIncorrect()

        new_hashed_password = self.auth_service.get_password_hash(user_request.password)
        user.hashed_password = new_hashed_password

        user.save(db)

    def delete_user(self, uuid: UUID, db: Session) -> None:
        user = self.database_service.get_record_by_id(uuid, db)
        user.delete(db)
