from typing import List, Optional
from uuid import UUID

from fastapi import Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import and_, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import BooleanClauseList

from app.models.data_enums import TaskPriority, TaskStatus
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskFilters, TaskUpdate, TaskView
from app.services.database_service import DatabaseService


class TaskService:
    def __init__(self):
        self.task_model = Task
        self.database_service = DatabaseService(self.task_model)
        self.task_model_name = self.task_model.__tablename__

    def _filter_task(
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        user_id: Optional[List[UUID]] = Query(None),
    ) -> BooleanClauseList:
        domains = []

        if status:
            domains.append(self.task_model.status == status)

        if priority:
            domains.append(self.task_model.priority == priority)

        if user_id:
            domains.append(self.task_model.user_id.in_(user_id))

        return and_(*domains)

    def get_all_tasks(self, task_filters: TaskFilters, db: Session) -> Page[TaskView]:
        domains = self._filter_task(
            status=task_filters.status,
            priority=task_filters.priority,
            user_id=task_filters.user_id,
        )

        query = select(self.task_model)

        if not isinstance(domains, BooleanClauseList):
            query = query.filter(domains)

        return paginate(db, query)

    def create_new_task(self, task: TaskCreate, db: Session) -> TaskView | None:
        new_task = self.task_model(**task.dict())
        new_task.save(db)

        return new_task

    def update_task_by_task_id(
        self, task_request: TaskUpdate, uuid: UUID, db: Session
    ) -> TaskView | None:
        task = self.database_service.get_record_by_id(uuid, self.task_model_name, db)

        for key, value in task_request.dict(exclude_unset=True).items():
            setattr(task, key, value)

        task.save(db)

        return task

    def delete_task(self, uuid: UUID, db: Session) -> None:
        task = self.database_service.get_record_by_id(uuid, self.task_model_name, db)
        task.delete(db)
