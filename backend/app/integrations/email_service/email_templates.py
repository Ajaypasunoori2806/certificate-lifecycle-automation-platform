class EmailTemplates:

    @staticmethod
    def certificate_expiry(
        certificate_name: str,
        expiry_date: str,
    ):

        subject = f"Certificate Expiry Reminder - {certificate_name}"

        body = f"""
Hello,

This is a reminder that the certificate

{certificate_name}

will expire on

{expiry_date}

Please renew it before the expiry date.

Thanks,
Certificate Lifecycle Automation Platform
"""

        return subject, body