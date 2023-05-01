import uuid

from sqlalchemy import Boolean, Column, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base_model import BaseModel


class User(Base, BaseModel):
    __tablename__ = "user"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    tasks = relationship("Task", back_populates="user")
    company_id = Column(Uuid, ForeignKey("company.id"), nullable=True)
    company = relationship("Company", back_populates="users")
