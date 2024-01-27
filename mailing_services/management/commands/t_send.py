import os

from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand



class Command(BaseCommand):
    def handle(self, *args, **options):
        print(os.getenv('USER'))
        send_mail('Тема', 'Тело письма', settings.EMAIL_HOST_USER, ['bersercer100@gmail.com.com'])
