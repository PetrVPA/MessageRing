from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from .models import Mailing


class MailingSender:
    """Класс для управления отправкой рассылки."""

    def __init__(self, mailing_instance):
        self.mailing = mailing_instance

    def send(self):
        """Основной метод отправки."""
        # 1. Проверка статуса (нельзя отправить то, что уже завершено)
        if self.mailing.status == 'finished':
            return False, "Рассылка уже завершена."

        # 2. Получаем список email-ов
        recipients = [r.email for r in self.mailing.recipients.all()]
        if not recipients:
            return False, "Нет получателей для отправки."

        # 3. Отправка
        try:
            send_mail(
                subject=self.mailing.message.subject,
                message=self.mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                fail_silently=False,
            )
        except Exception as e:
            return False, f"Ошибка отправки: {str(e)}"

        # 4. Обновление статуса модели
        self.mailing.status = 'started'
        if not self.mailing.first_sent_at:
            self.mailing.first_sent_at = timezone.now()
        self.mailing.save()

        return True, f"Успешно отправлено {len(recipients)} получателям."