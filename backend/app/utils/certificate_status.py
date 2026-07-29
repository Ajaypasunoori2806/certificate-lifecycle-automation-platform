from datetime import date


def calculate_certificate_status(
    expiry_date: date,
    reminder_days: int,
) -> str:
    """
    Calculate certificate status based on expiry date.
    """

    today = date.today()

    days_remaining = (expiry_date - today).days

    if days_remaining < 0:
        return "EXPIRED"

    if days_remaining <= reminder_days:
        return "EXPIRING_SOON"

    return "ACTIVE"