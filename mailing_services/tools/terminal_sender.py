from django.conf import settings
from django.core.mail import send_mail

send_mail('Тема', 'Тело письма', settings.EMAIL_HOST_USER, ['bersercer100@gmail.com.com'])
