from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.certificates.schemas import (
    CertificateCreate,
    CertificateResponse,
    CertificateUpdate,
)
from app.modules.certificates.service import CertificateService

router = APIRouter(
    prefix="/certificates",
    tags=["Certificates"],
)


@router.post(
    "/",
    response_model=CertificateResponse,
    status_code=201,
)
def create_certificate(
    certificate: CertificateCreate,
    db: Session = Depends(get_db),
):
    return CertificateService.create_certificate(
        db,
        certificate,
    )


@router.get(
    "/",
    response_model=list[CertificateResponse],
)
def get_all_certificates(
    application_id: int | None = None,
    status: str | None = None,
    environment: str | None = None,
    issuer: str | None = None,
    certificate_type: str | None = None,
    db: Session = Depends(get_db),
):
    if any([
        application_id is not None,
        status,
        environment,
        issuer,
        certificate_type,
    ]):
        return CertificateService.search_certificates(
            db=db,
            application_id=application_id,
            status=status,
            environment=environment,
            issuer=issuer,
            certificate_type=certificate_type,
        )

    return CertificateService.get_all_certificates(db)


@router.get(
    "/{certificate_id}",
    response_model=CertificateResponse,
)
def get_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
):
    return CertificateService.get_certificate(
        db,
        certificate_id,
    )


@router.put(
    "/{certificate_id}",
    response_model=CertificateResponse,
)
def update_certificate(
    certificate_id: int,
    certificate: CertificateUpdate,
    db: Session = Depends(get_db),
):
    return CertificateService.update_certificate(
        db,
        certificate_id,
        certificate,
    )


@router.delete(
    "/{certificate_id}",
)
def delete_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
):
    return CertificateService.delete_certificate(
        db,
        certificate_id,
    )