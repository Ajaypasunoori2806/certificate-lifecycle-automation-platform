from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class ApplicationBase(BaseModel):
    application_name: str
    owner_name: str
    owner_email: EmailStr
    environment: str
    business_unit: str
    description: str | None = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    application_name: str | None = None
    owner_name: str | None = None
    owner_email: EmailStr | None = None
    environment: str | None = None
    business_unit: str | None = None
    description: str | None = None
    is_active: bool | None = None


class ApplicationResponse(ApplicationBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)