from typing import List, Optional
from uuid import UUID

from fastapi import Query

from app.models.data_enums import TaskPriority, TaskStatus
from app.schemas.task import TaskFilters


def get_tasks_filters(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    user_id: Optional[List[UUID]] = Query(None),
) -> TaskFilters:
    return TaskFilters(status=status, priority=priority, user_id=user_id)
