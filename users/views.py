import random
import string
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render

from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.views import View

# Create your views here.
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.messages.views import SuccessMessageMixin

from config import settings
from users.models import User
from users.forms import UserRegisterForm, UserProfileForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    request.user.set_password(new_password)
    request.user.save()

    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    return redirect(reverse('catalog:index'))


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:registr_info')

    def form_valid(self, form):
        response = super().form_valid(form)
        new_user = form.save()
        # Создаем и сохраняем токен подтверждения
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
        new_user.email_verification_token = token
        new_user.save()
        # Отправляем письмо с подтверждением
        current_site = get_current_site(self.request)
        mail_subject = 'Подтвердите ваш аккаунт'
        message = (
            f'Добро пожаловать в магазин Экстремал, пожалуйста, завершите регистрацию перейди по ссылке\n'
            f'http://{current_site.domain}{reverse("users:verify_email", kwargs={"uid": new_user.pk, "token": token})}'
        )
        send_mail(subject=mail_subject, message=message, from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[new_user.email])
        return response


class VerifyEmailView(View):
    def get(self, request, uid, token):
        try:
            user = User.objects.get(pk=uid, email_verification_token=token)
            user.is_active = True
            user.save()
            return render(request, 'users/registr_success.html')  # Покажем сообщение о регистрации
        except User.DoesNotExist:
            return render(request, 'users/registr_failed.html')  # Покажем сообщение об ошибке


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def registr_info(request):
    return render(request, 'users/registr_info.html')


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('catalog:index')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'users/email/password_subject_reset_mail.txt'
    email_template_name = 'users/email/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('catalog:index')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context
