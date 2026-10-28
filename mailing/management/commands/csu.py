from django.core.management import BaseCommand
from gent.models import Gent

class Command(BaseCommand):
    def handle(self, *args, **options):
        user = Gent.objects.create(email='meteor@mail.ru')
        user.set_password('12345')
        user.name = 'Петр'
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
