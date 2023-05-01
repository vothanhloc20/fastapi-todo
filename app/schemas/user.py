import re
from typing import Optional
from uuid import UUID

from pydantic import BaseConfig, BaseModel, EmailStr, Field, validator

from app.schemas.company import CompanyView


class UserView(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    is_admin: bool
    is_active: bool
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[CompanyView] = None

    class Config(BaseConfig):
        orm_mode = True


class UserFilters(BaseModel):
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None
    company_id: Optional[str] = None


class UserBaseAuth(BaseModel):
    password: str = Field(alias="new_password")
    re_password: str

    class Config(BaseConfig):
        allow_population_by_field_name = True

    @validator("password")
    def verify_password_strength(cls, value):
        pattern = "^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[^A-Za-z0-9]).{8,}$"

        if not re.match(pattern, value):
            raise ValueError("Password is not strong enough, please check again")

        return value

    @validator("re_password")
    def verify_password_match(cls, value, values):
        if "password" in values and value != values["password"]:
            raise ValueError("Passwords do not match, please check again")

        return value


class UserBaseInformation(BaseModel):
    first_name: Optional[str] = Field(default=None, max_length=255)
    last_name: Optional[str] = Field(default=None, max_length=255)
    is_active: Optional[bool]
    is_admin: Optional[bool]
    company_id: Optional[UUID] = None


class UserCreate(UserBaseAuth, UserBaseInformation):
    email: EmailStr
    username: str


class UserUpdateInformation(UserBaseInformation):
    email: Optional[EmailStr] = None
    username: Optional[str] = None


class UserChangePassword(UserBaseAuth):
    current_password: str
