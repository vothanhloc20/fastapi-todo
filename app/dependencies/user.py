from typing import Optional

from app.schemas.user import UserFilters


def get_users_filters(
    is_admin: Optional[bool] = None,
    is_active: Optional[bool] = None,
    company_id: Optional[str] = None,
) -> UserFilters:
    return UserFilters(
        is_admin=is_admin,
        is_active=is_active,
        company_id=company_id,
    )
