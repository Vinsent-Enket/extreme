from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    email_verification_token = models.CharField(max_length=255, verbose_name='Токен для регистрации', **NULLABLE)
    email_is_verify = models.BooleanField(default=False, **NULLABLE, verbose_name='Емейл верифицирован')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=50, **NULLABLE, verbose_name='Страна')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    user_permissions = models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                              related_name='user_set',
                                              related_query_name='user', to='auth.permission',
                                              verbose_name='user permissions')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # def __str__(self):
    #     return int(self.pk)
