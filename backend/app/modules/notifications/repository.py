from datetime import datetime

from sqlalchemy.orm import Session

from app.modules.notifications.models import Notification
from app.modules.notifications.schemas import (
    NotificationCreate,
    NotificationUpdate,
)


class NotificationRepository:

    @staticmethod
    def create(
        db: Session,
        notification: NotificationCreate,
    ) -> Notification:

        db_notification = Notification(
            **notification.model_dump()
        )

        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)

        return db_notification

    @staticmethod
    def get_all(db: Session):
        return db.query(Notification).all()

    @staticmethod
    def get_by_id(
        db: Session,
        notification_id: int,
    ):
        return (
            db.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )

    @staticmethod
    def get_by_certificate_id(
        db: Session,
        certificate_id: int,
    ):
        return (
            db.query(Notification)
            .filter(
                Notification.certificate_id == certificate_id
            )
            .all()
        )

    @staticmethod
    def reminder_sent_today(
        db: Session,
        certificate_id: int,
    ):

        today = datetime.utcnow().date()

        return (
            db.query(Notification)
            .filter(
                Notification.certificate_id == certificate_id,
                Notification.notification_type == "EXPIRY_REMINDER",
                Notification.created_at >= today,
            )
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        db_notification: Notification,
        notification: NotificationUpdate,
    ):

        update_data = notification.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(db_notification, key, value)

        db.commit()
        db.refresh(db_notification)

        return db_notification

    @staticmethod
    def delete(
        db: Session,
        db_notification: Notification,
    ):

        db.delete(db_notification)
        db.commit()