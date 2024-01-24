from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='Admin@django.ru',
            first_name='Amon',
            last_name='Ra',
            is_staff=True,
            is_superuser=True
        )
        user.set_password('123qwe456rty')
        user.save()