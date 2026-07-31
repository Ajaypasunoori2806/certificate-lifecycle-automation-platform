from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.auth.permissions import require_admin
from app.database.session import get_db
from app.modules.applications.schemas import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
)
from app.modules.applications.service import ApplicationService

router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
)


@router.post(
    "/",
    response_model=ApplicationResponse,
    status_code=201,
)
def create_application(
    application: ApplicationCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return ApplicationService.create_application(db, application)


@router.get(
    "/",
    response_model=list[ApplicationResponse],
)
def get_all_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ApplicationService.get_all_applications(db)


@router.get(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def get_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ApplicationService.get_application(
        db,
        application_id,
    )


@router.put(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def update_application(
    application_id: int,
    application: ApplicationUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return ApplicationService.update_application(
        db,
        application_id,
        application,
    )


@router.delete(
    "/{application_id}",
)
def delete_application(
    application_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return ApplicationService.delete_application(
        db,
        application_id,
    )