from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.approvals.schemas import (
    ApprovalCreate,
    ApprovalResponse,
    ApprovalUpdate,
)
from app.modules.approvals.service import ApprovalService

router = APIRouter(
    prefix="/approvals",
    tags=["Approvals"],
)


@router.post(
    "/",
    response_model=ApprovalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_approval(
    approval: ApprovalCreate,
    db: Session = Depends(get_db),
):
    return ApprovalService.create_approval(
        db,
        approval,
    )


@router.get(
    "/",
    response_model=list[ApprovalResponse],
)
def get_all_approvals(
    db: Session = Depends(get_db),
):
    return ApprovalService.get_all_approvals(db)


@router.get(
    "/{approval_id}",
    response_model=ApprovalResponse,
)
def get_approval(
    approval_id: int,
    db: Session = Depends(get_db),
):
    return ApprovalService.get_approval(
        db,
        approval_id,
    )


@router.get(
    "/certificate/{certificate_id}",
    response_model=list[ApprovalResponse],
)
def get_certificate_approvals(
    certificate_id: int,
    db: Session = Depends(get_db),
):
    return ApprovalService.get_certificate_approvals(
        db,
        certificate_id,
    )


@router.put(
    "/{approval_id}",
    response_model=ApprovalResponse,
)
def update_approval(
    approval_id: int,
    approval: ApprovalUpdate,
    db: Session = Depends(get_db),
):
    return ApprovalService.update_approval(
        db,
        approval_id,
        approval,
    )


@router.delete(
    "/{approval_id}",
)
def delete_approval(
    approval_id: int,
    db: Session = Depends(get_db),
):
    return ApprovalService.delete_approval(
        db,
        approval_id,
    )