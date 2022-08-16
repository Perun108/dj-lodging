from djbooking.infrastructure.providers.email import email_provider


class EmailService:
    @classmethod
    def send_confirmation_code(cls, email, code):
        return email_provider.send_confirmation_code(email=email, code=code)
