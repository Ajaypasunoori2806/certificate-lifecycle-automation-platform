from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.modules.certificates.repository import CertificateRepository
from app.modules.notifications.repository import NotificationRepository
from app.modules.notifications.schemas import NotificationCreate
from app.modules.notifications.service import NotificationService


def check_expiring_certificates():
    print("Running certificate reminder scheduler...")

    db: Session = SessionLocal()

    try:
        certificates = CertificateRepository.get_all(db)

        today = datetime.utcnow().date()

        for certificate in certificates:

            days_left = (
                certificate.expiry_date - today
            ).days

            # Send reminder only if certificate is not expired
            # and is within reminder period
            if 0 <= days_left <= certificate.renewal_reminder_days:

                # Check if reminder has already been sent today
                existing_notification = (
                    NotificationRepository.reminder_sent_today(
                        db,
                        certificate.id,
                    )
                )

                if existing_notification:
                    print(
                        f"Reminder already sent today for {certificate.certificate_name}"
                    )
                    continue

                notification = NotificationCreate(
                    certificate_id=certificate.id,
                    recipient_email="ajaykumarpasunoori86@gmail.com",
                    subject=f"Certificate Expiry Reminder - {certificate.certificate_name}",
                    message=(
                        f"Hello,\n\n"
                        f"The certificate '{certificate.certificate_name}' "
                        f"will expire in {days_left} day(s).\n\n"
                        f"Expiry Date: {certificate.expiry_date}\n\n"
                        f"Please renew it before the expiry date.\n\n"
                        f"Thanks,\n"
                        f"Certificate Lifecycle Automation Platform"
                    ),
                    notification_type="EXPIRY_REMINDER",
                )

                NotificationService.create_notification(
                    db,
                    notification,
                )

                print(
                    f"Reminder email sent for {certificate.certificate_name}"
                )

    except Exception as e:
        print(f"Scheduler Error: {e}")

    finally:
        db.close()


scheduler = BackgroundScheduler()

scheduler.add_job(
    check_expiring_certificates,
    trigger="interval",
    minutes=1,  # Change to cron in production
)


def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        print("Scheduler started.")