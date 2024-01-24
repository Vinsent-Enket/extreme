# Generated by Django 4.2 on 2024-01-24 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='user',
            name='email_is_verify',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Емейл верифицирован'),
        ),
        migrations.AddField(
            model_name='user',
            name='email_verification_token',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Токен для регистрации'),
        ),
    ]