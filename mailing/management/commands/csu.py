from django.core.management import BaseCommand
from gent.models import Gent

class Command(BaseCommand):
    '''
        Создание супер пользователя с правами администратора и доступом в админку
    '''
    def handle(self, *args, **options):
        user = Gent.objects.create(email='meteor@mail.ru')
        user.set_password('12345')
        user.name = 'Петр'
        user.is_active = True
        user.is_staff = True        # <--- Изменили на True (право на доступ в админку)
        user.is_superuser = True    # <--- Изменили на True (права суперпользователя)
        user.save()
