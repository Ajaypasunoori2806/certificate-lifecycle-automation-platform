import smtplib
from email.message import EmailMessage

from app.core.config import settings


class SMTPService:

    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        message: str,
    ) -> bool:

        try:
            email = EmailMessage()

            email["From"] = settings.SMTP_FROM
            email["To"] = to_email
            email["Subject"] = subject

            email.set_content(message)

            with smtplib.SMTP(
                settings.SMTP_HOST,
                settings.SMTP_PORT,
            ) as smtp:

                smtp.starttls()

                smtp.login(
                    settings.SMTP_USERNAME,
                    settings.SMTP_PASSWORD,
                )

                smtp.send_message(email)

            return True

        except Exception as e:
            print(f"Email Error: {e}")
            return False