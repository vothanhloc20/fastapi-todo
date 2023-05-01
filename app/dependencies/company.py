from typing import Optional

from app.models.data_enums import CompanyMode
from app.schemas.company import CompanyFilters


def get_company_filters(
    mode: Optional[CompanyMode] = None, rating: Optional[str] = None
) -> CompanyFilters:
    return CompanyFilters(mode=mode, rating=rating)
