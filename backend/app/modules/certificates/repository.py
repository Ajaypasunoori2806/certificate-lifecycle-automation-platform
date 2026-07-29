from sqlalchemy.orm import Session

from app.modules.certificates.models import Certificate
from app.modules.certificates.schemas import (
    CertificateCreate,
    CertificateUpdate,
)


class CertificateRepository:

    @staticmethod
    def create(
        db: Session,
        certificate: CertificateCreate,
        status: str,
    ) -> Certificate:

        db_certificate = Certificate(
            **certificate.model_dump(),
            status=status,
        )

        db.add(db_certificate)
        db.commit()
        db.refresh(db_certificate)

        return db_certificate

    @staticmethod
    def get_all(db: Session):
        return db.query(Certificate).all()

    @staticmethod
    def search(
        db: Session,
        application_id: int | None = None,
        status: str | None = None,
        environment: str | None = None,
        issuer: str | None = None,
        certificate_type: str | None = None,
    ):

        query = db.query(Certificate)

        if application_id is not None:
            query = query.filter(
                Certificate.application_id == application_id
            )

        if status:
            query = query.filter(
                Certificate.status == status
            )

        if environment:
            query = query.filter(
                Certificate.environment == environment
            )

        if issuer:
            query = query.filter(
                Certificate.issuer == issuer
            )

        if certificate_type:
            query = query.filter(
                Certificate.certificate_type == certificate_type
            )

        return query.all()

    @staticmethod
    def get_by_id(
        db: Session,
        certificate_id: int,
    ):
        return (
            db.query(Certificate)
            .filter(Certificate.id == certificate_id)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        db_certificate: Certificate,
        certificate: CertificateUpdate,
    ):

        update_data = certificate.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(db_certificate, key, value)

        db.commit()
        db.refresh(db_certificate)

        return db_certificate

    @staticmethod
    def delete(
        db: Session,
        db_certificate: Certificate,
    ):

        db.delete(db_certificate)
        db.commit()