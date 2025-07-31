from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = "Cоздает суперпользователя"

    def handle(self, *args, **options):
        if not User.objects.filter(email="admin@sky.pro").exists():
            try:
                user = User(
                    email="admin@sky.pro",
                    is_superuser=True,
                    is_staff=True,
                    is_active=True,
                    first_name="Admin",
                    last_name="User",
                    phone="+1234567890",
                    role="ADMIN",
                )
                user.set_password("123qwe")
                user.save(force_insert=True)
                self.stdout.write(self.style.SUCCESS("Суперпользователь создан!"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка: {str(e)}"))
        else:
            self.stdout.write(self.style.WARNING("Суперпользователь уже существует!"))
