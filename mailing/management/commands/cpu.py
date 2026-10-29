from django.core.management import BaseCommand
from gent.models import Gent


class Command(BaseCommand):
    '''
    Создание простого пользователя без прав администратора и без доступа в админку
    '''
    def handle(self, *args, **options):
        # Создаем пользователя
        user = Gent.objects.create(email='meteor1@mail.ru')
        user.set_password('12345')
        user.name = 'Федя'

        # Настройки для обычного пользователя
        user.is_active = True
        user.is_staff = False  # <--- Изменили на False (нет доступа в админку)
        user.is_superuser = False  # <--- Изменили на False (нет прав суперпользователя)

        user.save()