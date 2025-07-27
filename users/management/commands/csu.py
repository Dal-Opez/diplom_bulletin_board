from django.core.management.base import BaseCommand
from users.models import User, ADMIN

class Command(BaseCommand):
    help = 'Cоздает суперпользователя'

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            user = User.objects.create(email="admin@sky.pro")
            user.set_password("123qwe")
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.role = ADMIN
            user.save()
            self.stdout.write(self.style.SUCCESS('Суперпользователь создан!'))