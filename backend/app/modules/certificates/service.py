from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.utils.certificate_status import calculate_certificate_status

from app.modules.applications.repository import ApplicationRepository
from app.modules.certificates.repository import CertificateRepository
from app.modules.certificates.schemas import (
    CertificateCreate,
    CertificateUpdate,
)


class CertificateService:

    @staticmethod
    def create_certificate(
        db: Session,
        certificate: CertificateCreate,
    ):

        application = ApplicationRepository.get_by_id(
            db,
            certificate.application_id,
        )

        if application is None:
            raise HTTPException(
                status_code=404,
                detail="Application not found.",
            )

        certificates = CertificateRepository.get_all(db)

        for cert in certificates:
            if cert.serial_number == certificate.serial_number:
                raise HTTPException(
                    status_code=400,
                    detail="Certificate serial number already exists.",
                )

        # Automatically calculate certificate status
        status = calculate_certificate_status(
            expiry_date=certificate.expiry_date,
            reminder_days=certificate.renewal_reminder_days,
        )

        return CertificateRepository.create(
            db=db,
            certificate=certificate,
            status=status,
        )

    @staticmethod
    def get_all_certificates(db: Session):
        return CertificateRepository.get_all(db)

    @staticmethod
    def search_certificates(
        db: Session,
        application_id: int | None = None,
        status: str | None = None,
        environment: str | None = None,
        issuer: str | None = None,
        certificate_type: str | None = None,
    ):
        return CertificateRepository.search(
            db=db,
            application_id=application_id,
            status=status,
            environment=environment,
            issuer=issuer,
            certificate_type=certificate_type,
        )

    @staticmethod
    def get_certificate(
        db: Session,
        certificate_id: int,
    ):

        certificate = CertificateRepository.get_by_id(
            db,
            certificate_id,
        )

        if certificate is None:
            raise HTTPException(
                status_code=404,
                detail="Certificate not found.",
            )

        return certificate

    @staticmethod
    def update_certificate(
        db: Session,
        certificate_id: int,
        certificate: CertificateUpdate,
    ):

        db_certificate = CertificateRepository.get_by_id(
            db,
            certificate_id,
        )

        if db_certificate is None:
            raise HTTPException(
                status_code=404,
                detail="Certificate not found.",
            )

        return CertificateRepository.update(
            db,
            db_certificate,
            certificate,
        )

    @staticmethod
    def delete_certificate(
        db: Session,
        certificate_id: int,
    ):

        db_certificate = CertificateRepository.get_by_id(
            db,
            certificate_id,
        )

        if db_certificate is None:
            raise HTTPException(
                status_code=404,
                detail="Certificate not found.",
            )

        CertificateRepository.delete(
            db,
            db_certificate,
        )

        return {
            "message": "Certificate deleted successfully."
        }