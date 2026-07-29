from sqlalchemy.orm import Session

from app.modules.approvals.models import Approval
from app.modules.approvals.schemas import (
    ApprovalCreate,
    ApprovalUpdate,
)


class ApprovalRepository:

    @staticmethod
    def create(
        db: Session,
        approval: ApprovalCreate,
    ) -> Approval:

        db_approval = Approval(
            **approval.model_dump()
        )

        db.add(db_approval)
        db.commit()
        db.refresh(db_approval)

        return db_approval

    @staticmethod
    def get_all(db: Session):
        return db.query(Approval).all()

    @staticmethod
    def get_by_id(
        db: Session,
        approval_id: int,
    ):
        return (
            db.query(Approval)
            .filter(Approval.id == approval_id)
            .first()
        )

    @staticmethod
    def get_by_certificate_id(
        db: Session,
        certificate_id: int,
    ):
        return (
            db.query(Approval)
            .filter(
                Approval.certificate_id == certificate_id
            )
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        db_approval: Approval,
        approval: ApprovalUpdate,
    ):

        update_data = approval.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(db_approval, key, value)

        db.commit()
        db.refresh(db_approval)

        return db_approval

    @staticmethod
    def delete(
        db: Session,
        db_approval: Approval,
    ):

        db.delete(db_approval)
        db.commit()