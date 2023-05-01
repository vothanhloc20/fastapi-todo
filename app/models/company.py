import uuid

from sqlalchemy import Column, Enum, SmallInteger, String, Uuid
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base_model import BaseModel
from app.models.data_enums import CompanyMode


class Company(Base, BaseModel):
    __tablename__ = "company"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    mode = Column(Enum(CompanyMode), nullable=False, default=CompanyMode.Active)
    rating = Column(SmallInteger, default=0)
    users = relationship("User", back_populates="company")
