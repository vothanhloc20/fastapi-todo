from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.constants.constants import RouteTagConstants
from app.constants.routers import ROUTE_AUTH, ROUTE_TOKEN
from app.services.auth_service import AuthService
from app.services.database_service import DatabaseService

router = APIRouter(prefix=ROUTE_AUTH, tags=[RouteTagConstants.AUTH_TAG])
database_service = DatabaseService()
auth_service = AuthService()
session = database_service.get_session()


@router.post(ROUTE_TOKEN)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = session
):
    username = (form_data.username,)
    password = form_data.password
    user = auth_service.authenticate_user(username, password, db)

    return auth_service.create_access_token(user)
