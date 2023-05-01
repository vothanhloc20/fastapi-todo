from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import LocalSession
from app.services.exception_service import ExceptionService


class DatabaseService:
    def __init__(self, model: Optional[any] = None):
        self.local_session = LocalSession()
        self.model = model

    def _get_db_context(self):
        db = self.local_session

        try:
            yield db
        finally:
            db.close()

    def get_session(self):
        return Depends(self._get_db_context)

    def get_record_by_id(self, uuid: UUID, table_name: str, db: Session):
        record = db.query(self.model).filter(self.model.id == uuid).first()

        if not record:
            raise ExceptionService().NotFoundException(table_name.capitalize())

        return record
