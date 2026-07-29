from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.integrations.email_service.smtp_service import SMTPService
from app.modules.certificates.repository import CertificateRepository
from app.modules.notifications.repository import NotificationRepository
from app.modules.notifications.schemas import (
    NotificationCreate,
    NotificationUpdate,
)


class NotificationService:

    @staticmethod
    def create_notification(
        db: Session,
        notification: NotificationCreate,
    ):

        # Verify certificate exists
        certificate = CertificateRepository.get_by_id(
            db,
            notification.certificate_id,
        )

        if certificate is None:
            raise HTTPException(
                status_code=404,
                detail="Certificate not found.",
            )

        # Save notification first
        db_notification = NotificationRepository.create(
            db,
            notification,
        )

        # Send email
        email_sent = SMTPService.send_email(
            to_email=notification.recipient_email,
            subject=notification.subject,
            message=notification.message,
        )

        # Update notification status
        if email_sent:

            update_notification = NotificationUpdate(
                status="SENT",
                is_sent=True,
            )

        else:

            update_notification = NotificationUpdate(
                status="FAILED",
                is_sent=False,
            )

        return NotificationRepository.update(
            db,
            db_notification,
            update_notification,
        )

    @staticmethod
    def get_all_notifications(
        db: Session,
    ):
        return NotificationRepository.get_all(db)

    @staticmethod
    def get_notification(
        db: Session,
        notification_id: int,
    ):

        db_notification = NotificationRepository.get_by_id(
            db,
            notification_id,
        )

        if db_notification is None:
            raise HTTPException(
                status_code=404,
                detail="Notification not found.",
            )

        return db_notification

    @staticmethod
    def get_certificate_notifications(
        db: Session,
        certificate_id: int,
    ):
        return NotificationRepository.get_by_certificate_id(
            db,
            certificate_id,
        )

    @staticmethod
    def update_notification(
        db: Session,
        notification_id: int,
        notification: NotificationUpdate,
    ):

        db_notification = NotificationRepository.get_by_id(
            db,
            notification_id,
        )

        if db_notification is None:
            raise HTTPException(
                status_code=404,
                detail="Notification not found.",
            )

        update_data = notification.model_dump(
            exclude_unset=True
        )

        # Automatically set sent_at
        if (
            "is_sent" in update_data
            and update_data["is_sent"] is True
        ):
            db_notification.sent_at = datetime.utcnow()

        return NotificationRepository.update(
            db,
            db_notification,
            notification,
        )

    @staticmethod
    def delete_notification(
        db: Session,
        notification_id: int,
    ):

        db_notification = NotificationRepository.get_by_id(
            db,
            notification_id,
        )

        if db_notification is None:
            raise HTTPException(
                status_code=404,
                detail="Notification not found.",
            )

        NotificationRepository.delete(
            db,
            db_notification,
        )

        return {
            "message": "Notification deleted successfully."
        }