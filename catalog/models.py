from datetime import datetime

import django
from django.conf import settings
from django.db import models
from django.utils import timezone
from pytils.translit import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from users.models import User

# Create your models here.
NULLABLE = {'blank': True, 'null': True}
now = django.utils.timezone.now
fobidden_words = (
    "казино", "криптовалюта",
    "крипта", "биржа",
    "дешево", "бесплатно",
    "обман", "полиция",
    "радар"
)


def validate_even(value):
    if value in settings.FORBIDDEN_WORDS:
        raise ValidationError(
            _("использование слова {{{%(value)s}}} запрещено"),
            params={"value": value},
        )


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название категории')
    description = models.CharField(max_length=250, verbose_name='Описание категории')

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'  # Настройка для наименования одного объекта
        verbose_name_plural = 'категории'  # Настройка для наименования набора объектов
        ordering = ('description',)


class Blog(models.Model):
    header = models.CharField(max_length=150, verbose_name='Заголовок поста')
    slug = models.CharField(max_length=150, verbose_name='Слаг', **NULLABLE, default=slugify(header))
    text = models.TextField(verbose_name='Содержание')
    preview = models.ImageField(upload_to='blog/', verbose_name='Превью', **NULLABLE)
    date_of_creation = models.DateField(verbose_name='Дата создания', default=now)
    is_published = models.BooleanField(verbose_name='Было опубликовано', default=True)
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return f'{self.header}'

    class Meta:
        verbose_name = 'пост'  # Настройка для наименования одного объекта
        verbose_name_plural = 'посты'  # Настройка для наименования набора объектов
        ordering = ('header', 'date_of_creation')


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название товара', validators=[validate_even])
    description = models.CharField(max_length=250, verbose_name='Описание товара', validators=[validate_even])
    images = models.ImageField(upload_to='product/', verbose_name='Картинка', **NULLABLE,
                               default='apu-upal-i-uronil-edu.jpg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    proprietor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                                   verbose_name='Владелец')

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    date_of_creation = models.DateField(verbose_name='Дата создания', default=now)
    date_of_change = models.DateField(verbose_name='Дата изменения', default=now)
    # version = models.ManyToOneRel

    published_status = models.BooleanField(default=False, verbose_name='Было опубликовано')

    # posts = models.ManyToManyField(Blog, verbose_name='Отзывы о товаре', **NULLABLE)

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.name}'

    class Meta:
        verbose_name = 'товар'  # Настройка для наименования одного объекта
        verbose_name_plural = 'товары'  # Настройка для наименования набора объектов
        ordering = ('id',)
        permissions = [('set_published_status', 'Can publish product'),
                       ('change_description', 'Can change description'),
                       ('change_category', 'Can change category'), ]


class Version(models.Model):
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Название продукта')
    version_number = models.IntegerField(verbose_name='Номер версии')
    version_name = models.CharField(max_length=50, verbose_name='Название версии')
    is_active_version = models.BooleanField(verbose_name='Активная ли версия', default=False)

    def __str__(self):
        return f'Версия {self.version_name}, продукта {self.product_name}'
