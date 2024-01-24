from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, VerifyEmailView, registr_info, generate_new_password, \
     UserForgotPasswordView, UserPasswordResetConfirmView

app_name = UsersConfig.name

urlpatterns = [
    path('registr_info/', registr_info, name='registr_info'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify_email/<str:uid>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]
