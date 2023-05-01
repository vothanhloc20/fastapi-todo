import uuid

from sqlalchemy import Column, Enum, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base_model import BaseModel
from app.models.data_enums import TaskPriority, TaskStatus


class Task(Base, BaseModel):
    __tablename__ = "task"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    summary = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.NotStarted)
    priority = Column(Enum(TaskPriority), nullable=True)
    user_id = Column(Uuid, ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="tasks")
