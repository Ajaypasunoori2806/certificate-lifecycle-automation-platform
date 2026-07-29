from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.approvals.repository import ApprovalRepository
from app.modules.approvals.schemas import (
    ApprovalCreate,
    ApprovalUpdate,
)
from app.modules.certificates.repository import CertificateRepository


class ApprovalService:

    @staticmethod
    def create_approval(
        db: Session,
        approval: ApprovalCreate,
    ):

        # Verify certificate exists
        certificate = CertificateRepository.get_by_id(
            db,
            approval.certificate_id,
        )

        if certificate is None:
            raise HTTPException(
                status_code=404,
                detail="Certificate not found.",
            )

        return ApprovalRepository.create(
            db,
            approval,
        )

    @staticmethod
    def get_all_approvals(db: Session):
        return ApprovalRepository.get_all(db)

    @staticmethod
    def get_approval(
        db: Session,
        approval_id: int,
    ):

        approval = ApprovalRepository.get_by_id(
            db,
            approval_id,
        )

        if approval is None:
            raise HTTPException(
                status_code=404,
                detail="Approval not found.",
            )

        return approval

    @staticmethod
    def get_certificate_approvals(
        db: Session,
        certificate_id: int,
    ):

        return ApprovalRepository.get_by_certificate_id(
            db,
            certificate_id,
        )

    @staticmethod
    def update_approval(
        db: Session,
        approval_id: int,
        approval: ApprovalUpdate,
    ):

        db_approval = ApprovalRepository.get_by_id(
            db,
            approval_id,
        )

        if db_approval is None:
            raise HTTPException(
                status_code=404,
                detail="Approval not found.",
            )

        update_data = approval.model_dump(exclude_unset=True)

        # Automatically populate approved_at
        if (
            "approval_status" in update_data
            and update_data["approval_status"] == "APPROVED"
        ):
            db_approval.approved_at = datetime.utcnow()

        return ApprovalRepository.update(
            db,
            db_approval,
            approval,
        )

    @staticmethod
    def delete_approval(
        db: Session,
        approval_id: int,
    ):

        db_approval = ApprovalRepository.get_by_id(
            db,
            approval_id,
        )

        if db_approval is None:
            raise HTTPException(
                status_code=404,
                detail="Approval not found.",
            )

        ApprovalRepository.delete(
            db,
            db_approval,
        )

        return {
            "message": "Approval deleted successfully."
        }