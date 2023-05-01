from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from starlette import status

from app.constants.constants import RouteTagConstants
from app.constants.routers import (
    ROUTE_CREATE,
    ROUTE_DELETE_BY_ID,
    ROUTE_TASK,
    ROUTE_UPDATE_BY_ID,
)
from app.dependencies.task import get_tasks_filters
from app.models.user import User
from app.schemas.task import TaskCreate, TaskFilters, TaskUpdate, TaskView
from app.services.auth_service import AuthService
from app.services.database_service import DatabaseService
from app.services.task_service import TaskService
from app.utils.auth import admin_permission_required

router = APIRouter(prefix=ROUTE_TASK, tags=[RouteTagConstants.TASK_TAG])

database_service = DatabaseService()
auth_service = AuthService()
task_service = TaskService()

session = database_service.get_session()
token_interceptor = auth_service.get_token_interceptor()


@router.get("", response_model=Page[TaskView])
@admin_permission_required
def get_all_tasks(
    task_filters: TaskFilters = Depends(get_tasks_filters),
    user: User = token_interceptor,
    db: Session = session,
) -> Page[TaskView]:
    result = task_service.get_all_tasks(task_filters, db)
    return result


@router.post(ROUTE_CREATE, response_model=TaskView, status_code=status.HTTP_201_CREATED)
def create_new_task(task: TaskCreate, db: Session = session) -> TaskView:
    result = task_service.create_new_task(task, db)
    return result


@router.put(ROUTE_UPDATE_BY_ID, response_model=TaskView)
def update_task_by_task_id(
    task: TaskUpdate, uuid: UUID, db: Session = session
) -> TaskView:
    result = task_service.update_task_by_task_id(task, uuid, db)
    return result


@router.delete(ROUTE_DELETE_BY_ID, status_code=status.HTTP_204_NO_CONTENT)
def delete_task(uuid: UUID, db: Session = session) -> None:
    task_service.delete_task(uuid, db)
