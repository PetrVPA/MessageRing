import logging

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Attempt

logger = logging.getLogger(__name__)


class MailingSender:
    """Отправляет рассылку и сохраняет историю попыток по каждому получателю."""

    def __init__(self, mailing):
        self.mailing = mailing
        self.success_count = 0
        self.error_count = 0

    def _time_error(self):
        """Возвращает текст ошибки, если сейчас отправлять нельзя."""
        if not self.mailing.start_time or not self.mailing.end_time:
            return 'У рассылки не указаны дата и время начала/окончания.'

        now = timezone.now()

        if now < self.mailing.start_time:
            start = timezone.localtime(self.mailing.start_time)
            return (
                'Рассылка ещё не началась. '
                f'Время начала: {start:%d.%m.%Y %H:%M}.'
            )

        if now > self.mailing.end_time:
            end = timezone.localtime(self.mailing.end_time)
            return (
                'Время рассылки истекло. '
                f'Время окончания: {end:%d.%m.%Y %H:%M}.'
            )

        return None

    def _validate(self):
        """Проверяет данные перед отправкой."""
        if not self.mailing.message_id:
            return 'У рассылки не указано сообщение.'

        error = self._time_error()
        if error:
            return error

        if not self.mailing.recipients.exists():
            return 'Нет получателей для отправки.'

        return None

    def send(self):
        error = self._validate()
        if error:
            return False, error

        recipients = list(self.mailing.recipients.all())
        attempts = []
        attempt_time = timezone.now()

        for recipient in recipients:
            try:
                sent_count = send_mail(
                    subject=self.mailing.message.subject,
                    message=self.mailing.message.body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )
            except Exception as exc:
                self.error_count += 1
                response = str(exc)
                logger.exception(
                    'Ошибка отправки письма получателю %s по рассылке %s',
                    recipient.email,
                    self.mailing.pk,
                )
                attempts.append(
                    Attempt(
                        mailing=self.mailing,
                        recipient=recipient,
                        attempt_time=attempt_time,
                        status=Attempt.STATUS_FAILED,
                        server_response=response,
                    )
                )
            else:
                if sent_count:
                    self.success_count += 1
                    attempts.append(
                        Attempt(
                            mailing=self.mailing,
                            recipient=recipient,
                            attempt_time=attempt_time,
                            status=Attempt.STATUS_SUCCESS,
                            server_response='Письмо отправлено.',
                        )
                    )
                else:
                    self.error_count += 1
                    attempts.append(
                        Attempt(
                            mailing=self.mailing,
                            recipient=recipient,
                            attempt_time=attempt_time,
                            status=Attempt.STATUS_FAILED,
                            server_response='Почтовый сервер не подтвердил отправку.',
                        )
                    )

        # Сохраняем все попытки одним запросом.
        Attempt.objects.bulk_create(attempts)

        self.mailing.update_status()

        result_message = (
            f'Отправка завершена. Успешно: {self.success_count}, '
            f'ошибок: {self.error_count}.'
        )
        return self.error_count == 0, result_message