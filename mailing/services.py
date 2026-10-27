import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

class MailingSender:
    def __init__(self, mailing):
        self.mailing = mailing
        self.success_count = 0
        self.error_count = 0

    def send(self):
        if self.mailing.status == 'finished':
            return False, "Рассылка уже завершена."

        recipients = [r.email for r in self.mailing.recipients.all()]
        if not recipients:
            return False, "Нет получателей для отправки."

        try:
            send_mail(
                subject=self.mailing.message.subject,
                message=self.mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                fail_silently=False,
            )
            self.success_count = len(recipients)
        except Exception as e:
            self.error_count = len(recipients)
            return False, f"Ошибка отправки: {str(e)}"

        self.mailing.status = 'started'
        self.mailing.save()
        return True, f"Успешно отправлено писем: {self.success_count}"
