from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Удаляет пользователя по указанному email'

    def add_arguments(self, parser):
        # Добавляем обязательный аргумент email
        parser.add_argument('email', type=str, help='Email пользователя для удаления')

    def handle(self, *args, **options):
        email = options['email']
        User = get_user_model()

        try:
            # Ищем пользователя по email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Если не нашли, выбрасываем понятную ошибку
            raise CommandError(f'Пользователь с email "{email}" не найден.')

        # Удаляем пользователя
        user.delete()
        self.stdout.write(
            self.style.SUCCESS(f'Пользователь с email "{email}" успешно удален.')
        )