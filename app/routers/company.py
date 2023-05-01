from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from starlette import status

from app.constants.constants import RouteTagConstants
from app.constants.routers import (
    ROUTE_COMPANY,
    ROUTE_CREATE,
    ROUTE_DELETE_BY_ID,
    ROUTE_UPDATE_BY_ID,
)
from app.dependencies.company import get_company_filters
from app.schemas.company import (
    CompanyCreate,
    CompanyFilters,
    CompanyUpdateInformation,
    CompanyView,
)
from app.services.company_service import CompanyService
from app.services.database_service import DatabaseService

router = APIRouter(prefix=ROUTE_COMPANY, tags=[RouteTagConstants.COMPANY_TAG])
database_service = DatabaseService()
company_service = CompanyService()
session = database_service.get_session()


@router.get("", response_model=Page[CompanyView])
def get_all_company(
    company_filters: CompanyFilters = Depends(get_company_filters),
    db: Session = session,
) -> Page[CompanyView]:
    result = company_service.get_all_company(company_filters, db)
    return result


@router.post(
    ROUTE_CREATE, response_model=CompanyView, status_code=status.HTTP_201_CREATED
)
def create_new_company(company: CompanyCreate, db: Session = session) -> CompanyView:
    result = company_service.create_new_company(company, db)
    return result


@router.put(ROUTE_UPDATE_BY_ID, response_model=CompanyView)
def update_information_company_by_company_id(
    company_request: CompanyUpdateInformation, uuid: UUID, db: Session = session
) -> CompanyView:
    result = company_service.update_information_company_by_company_id(
        company_request, uuid, db
    )
    return result


@router.delete(ROUTE_DELETE_BY_ID)
def delete_company(uuid: UUID, db: Session = session) -> None:
    company_service.delete_company(uuid, db)
