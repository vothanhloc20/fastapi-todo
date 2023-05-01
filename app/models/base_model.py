import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Uuid
from sqlalchemy.orm import Session


class BaseModel:
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, unique=True)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow())

    def save(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)

    def delete(self, db: Session):
        db.delete(self)
        db.commit()
