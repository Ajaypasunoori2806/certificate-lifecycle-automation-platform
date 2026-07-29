from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class NotificationBase(BaseModel):
    certificate_id: int
    recipient_email: EmailStr
    subject: str
    message: str
    notification_type: str


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    recipient_email: Optional[EmailStr] = None
    subject: Optional[str] = None
    message: Optional[str] = None
    notification_type: Optional[str] = None
    status: Optional[str] = None
    is_sent: Optional[bool] = None


class NotificationResponse(NotificationBase):
    id: int
    status: str
    is_sent: bool
    sent_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)