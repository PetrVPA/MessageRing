from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Создает суперпользователя, если его еще нет'

    def add_arguments(self, parser):
        # Добавляем аргументы командной строки
        parser.add_argument('username', type=str, help='Имя пользователя')
        parser.add_argument('email', type=str, help='Email')
        parser.add_argument('password', type=str, help='Пароль')

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        email = options['email']
        password = options['password']

        # Проверяем, существует ли пользователь
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Пользователь {username} уже существует.'))
            return

        # Создаем суперпользователя
        User.objects.create_superuser(username=username, email=email, password=password)

        # Выводим сообщение об успехе (зеленым цветом)
        self.stdout.write(self.style.SUCCESS(f'Суперпользователь {username} успешно создан!'))