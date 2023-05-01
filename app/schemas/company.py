from typing import Optional
from uuid import UUID

from pydantic import BaseConfig, BaseModel, Field

from app.models.data_enums import CompanyMode


class CompanyView(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    mode: CompanyMode = Field(default=CompanyMode.Active)
    rating: Optional[int] = Field(default=0, ge=0, le=5)

    class Config(BaseConfig):
        orm_mode = True


class CompanyCreate(BaseModel):
    name: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)

    class Config(BaseConfig):
        schema_extra = {
            "example": {"name": "Company Name", "description": "Company Description"}
        }


class CompanyUpdateInformation(BaseModel):
    name: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None)
    mode: Optional[CompanyMode] = Field(default=CompanyMode.Active)
    rating: Optional[int] = Field(default=0, ge=0, le=5)

    class Config(BaseConfig):
        schema_extra = {
            "example": {
                "name": "Company Name",
                "description": "Company Description",
                "mode": CompanyMode.TemporarilyClosed,
                "rating": 5,
            }
        }


class CompanyFilters(BaseModel):
    mode: Optional[CompanyMode] = Field(default=None)
    rating: Optional[int] = Field(default=None, ge=0, le=5)
