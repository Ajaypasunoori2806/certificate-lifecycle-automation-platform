from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.notifications.schemas import (
    NotificationCreate,
    NotificationResponse,
    NotificationUpdate,
)
from app.modules.notifications.service import NotificationService

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.post(
    "/",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
):
    return NotificationService.create_notification(
        db,
        notification,
    )


@router.get(
    "/",
    response_model=list[NotificationResponse],
)
def get_all_notifications(
    db: Session = Depends(get_db),
):
    return NotificationService.get_all_notifications(db)


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
)
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    return NotificationService.get_notification(
        db,
        notification_id,
    )


@router.get(
    "/certificate/{certificate_id}",
    response_model=list[NotificationResponse],
)
def get_certificate_notifications(
    certificate_id: int,
    db: Session = Depends(get_db),
):
    return NotificationService.get_certificate_notifications(
        db,
        certificate_id,
    )


@router.put(
    "/{notification_id}",
    response_model=NotificationResponse,
)
def update_notification(
    notification_id: int,
    notification: NotificationUpdate,
    db: Session = Depends(get_db),
):
    return NotificationService.update_notification(
        db,
        notification_id,
        notification,
    )


@router.delete(
    "/{notification_id}",
)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    return NotificationService.delete_notification(
        db,
        notification_id,
    )