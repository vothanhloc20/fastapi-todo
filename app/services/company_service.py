from typing import Optional
from uuid import UUID

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import and_, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import BooleanClauseList

from app.models.company import Company
from app.models.data_enums import CompanyMode
from app.schemas.company import (
    CompanyCreate,
    CompanyFilters,
    CompanyUpdateInformation,
    CompanyView,
)
from app.services.database_service import DatabaseService


class CompanyService:
    def __init__(self):
        self.company_model = Company
        self.database_service = DatabaseService(self.company_model)
        self.company_model_name = self.company_model.__tablename__

    def _filter_company(
        self, mode: Optional[CompanyMode] = None, rating: Optional[str] = None
    ) -> BooleanClauseList:
        domains = []

        if mode:
            domains.append(self.company_model.mode == mode)

        if rating:
            domains.append(self.company_model.rating == rating)

        return and_(*domains)

    def get_all_company(
        self, company_filters: CompanyFilters, db: Session
    ) -> Page[CompanyView]:
        domains = self._filter_company(
            mode=company_filters.mode, rating=company_filters.rating
        )

        query = select(self.company_model)

        if not isinstance(domains, BooleanClauseList):
            query = query.filter(domains)

        return paginate(db, query)

    def create_new_company(
        self, company_request: CompanyCreate, db: Session
    ) -> CompanyView | None:
        new_company = self.company_model(**company_request.dict())
        new_company.save(db)

        return new_company

    def update_information_company_by_company_id(
        self, company_request: CompanyUpdateInformation, uuid: UUID, db: Session
    ) -> CompanyView | None:
        company = self.database_service.get_record_by_id(
            uuid, self.company_model_name, db
        )

        for key, value in company_request.dict(exclude_unset=True).items():
            setattr(company, key, value)

        company.save(db)

        return company

    def delete_company(self, uuid: UUID, db: Session) -> None:
        company = self.database_service.get_record_by_id(
            uuid, self.company_model_name, db
        )
        company.delete(db)
