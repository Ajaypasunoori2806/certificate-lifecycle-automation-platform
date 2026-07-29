from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class ApprovalBase(BaseModel):
    certificate_id: int
    approver_name: str
    approver_email: EmailStr
    comments: Optional[str] = None


class ApprovalCreate(ApprovalBase):
    pass


class ApprovalUpdate(BaseModel):
    approver_name: Optional[str] = None
    approver_email: Optional[EmailStr] = None
    approval_status: Optional[str] = None
    comments: Optional[str] = None


class ApprovalResponse(ApprovalBase):
    id: int
    approval_status: str
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)