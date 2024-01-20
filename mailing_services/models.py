import django
from django.db import models
from django.utils import timezone
from pytils.translit import slugify

NULLABLE = {'blank': True, 'null': True}
now = django.utils.timezone.now


class Client(models.Model):
    email = models.EmailField(verbose_name='Email клиента')
    name = models.CharField(max_length=100, verbose_name='ФИО клиента')
    comments = models.CharField(max_length=200, verbose_name='Комментарии')
    slug = models.CharField(max_length=150, verbose_name='Слаг', **NULLABLE, default=slugify(name))

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиента'


class Message(models.Model):
    header = models.CharField(max_length=100, verbose_name='Тема email')
    body = models.TextField(verbose_name='Текст сообщения')

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'

    def __str__(self):
        return self.header


class Mailing(models.Model):
    period = [
        ('once_a_day', 'Раз в день'),
        ('once_a_week', 'Раз в неделю'),
        ('once_a_month', 'Раз в месяц')
    ]

    status = [
        ('created', 'создана'),
        ('in_work', 'в работе'),
        ('stopped', 'остановлена')

    ]
    time = models.TimeField(verbose_name='время рассылки', default='9:00')
    create_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    regularity = models.CharField(choices=period, default='once_a_day', verbose_name='Периодичность')
    status = models.CharField(choices=status, max_length=50, verbose_name='Статус', default=status[0])
    client = models.ManyToManyField(Client, verbose_name='Клиент')
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, verbose_name='Сообщение', **NULLABLE)

    def __str__(self):
        return f'{self.time}, {self.regularity}'

    def get_clients(self):
        client_list = self.client.get_queryset()
        client_str = ''
        for client in client_list:
            client_str += ', ' + client.name
        return client_str.lstrip(', ')

    get_clients.short_description = 'клиенты'

    class Meta:
        verbose_name = 'Рассылка для клиентов'
        verbose_name_plural = 'Рассылки'


class MailingLogs(models.Model):
    STATUS = [
        ('Success', 'успешно'),
        ('Failure', 'отказ')
    ]

    data_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отправки')
    status = models.CharField(max_length=100, choices=STATUS, verbose_name='Статус попытки')
    server_response = models.TextField(verbose_name='Ответ почтового сервера', **NULLABLE)
    mailing = models.ForeignKey(Mailing, on_delete=models.SET_NULL, verbose_name='Рассылка', **NULLABLE)

    class Meta:
        verbose_name = 'лог отправки письма'
        verbose_name_plural = 'логи отправок писем'

    def __str__(self):
        return f'Лог {self.pk}'
