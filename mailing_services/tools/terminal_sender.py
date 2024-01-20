import os

from django.core.mail import send_mail
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reminder.settings')

send_mail(
    subject=input('Введите тему сообщения--> '),
    message=input('Введите текст сообщения--> '),
    from_email=input('Введите ваш email--> '),
    recipient_list=list(input('Введите email получателя--> '),)
)
