from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CertificateBase(BaseModel):
    application_id: int
    certificate_name: str
    common_name: str
    issuer: str
    serial_number: str
    certificate_type: str
    environment: str
    issued_date: date
    expiry_date: date
    renewal_reminder_days: int = 30
    is_active: bool = True


class CertificateCreate(CertificateBase):
    pass


class CertificateUpdate(BaseModel):
    certificate_name: Optional[str] = None
    common_name: Optional[str] = None
    issuer: Optional[str] = None
    serial_number: Optional[str] = None
    certificate_type: Optional[str] = None
    environment: Optional[str] = None
    issued_date: Optional[date] = None
    expiry_date: Optional[date] = None
    renewal_reminder_days: Optional[int] = None
    is_active: Optional[bool] = None


class CertificateResponse(CertificateBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)