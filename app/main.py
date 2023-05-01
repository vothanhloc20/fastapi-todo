from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from app.middlewares.middleware import handle_error
from app.routers.auth import router as auth_router
from app.routers.company import router as company_router
from app.routers.task import router as task_router
from app.routers.user import router as user_router
from app.settings import settings

app = FastAPI()

"""Add middleware"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

app.middleware("http")(handle_error)

"""Add router"""
app.include_router(user_router)
app.include_router(task_router)
app.include_router(auth_router)
app.include_router(company_router)

"""Add pagination"""
add_pagination(app)
