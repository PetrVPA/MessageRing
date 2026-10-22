from django.core.management.base import BaseCommand
from mailing.models import Mailing
from mailing.services import MailingSender  # Импортируем наш класс


class Command(BaseCommand):
    help = 'Отправляет конкретную рассылку по её ID'

    def add_arguments(self, parser):
        # Команда будет принимать ID рассылки как аргумент
        parser.add_argument('mailing_id', type=int, help='ID рассылки')

    def handle(self, *args, **options):
        mailing_id = options['mailing_id']

        try:
            # Ищем рассылку в базе
            mailing = Mailing.objects.get(pk=mailing_id)
        except Mailing.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Рассылка с ID {mailing_id} не найдена.'))
            return

        # Вызываем наш сервис отправки
        sender = MailingSender(mailing)
        success, message = sender.send()

        if success:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stdout.write(self.style.ERROR(message))