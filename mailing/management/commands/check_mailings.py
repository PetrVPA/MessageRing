from django.core.management.base import BaseCommand
from django.utils import timezone
from mailing.models import Mailing
from mailing.services import MailingSender


class Command(BaseCommand):
    help = 'Проверяет время начала рассылок и запускает их'

    def handle(self, *args, **options):
        now = timezone.now()

        # Ищем рассылки, которые должны начаться прямо сейчас или уже начались
        # Статус 'created', время старта меньше или равно текущему моменту
        mailings_to_start = Mailing.objects.filter(
            status='created',
            start_time__lte=now,
            end_time__gte=now  # И время окончания еще не прошло
        )

        if not mailings_to_start.exists():
            self.stdout.write("Нет рассылок для запуска.")
            return

        for mailing in mailings_to_start:
            self.stdout.write(f"Запуск рассылки ID: {mailing.id}...")

            # Меняем статус на 'started' перед отправкой
            mailing.status = 'started'
            mailing.save(update_fields=['status'])

            # Вызываем наш сервис
            sender = MailingSender(mailing)
            success, message = sender.send()

            if success:
                self.stdout.write(self.style.SUCCESS(message))
            else:
                self.stdout.write(self.style.ERROR(message))