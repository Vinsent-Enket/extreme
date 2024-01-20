from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from mailing_services.apps import MailingServicesConfig
from mailing_services.views import ClientCreateView, contacts, ClientListView, ClientUpdateView, ClientDeleteView, \
    MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, MessageListView, MessageCreateView, \
    MessageUpdateView, MessageDeleteView, MailingLogListView

app_name = MailingServicesConfig.name

urlpatterns = [
    path('contacts', contacts, name='contacts'),
    path('send_contacts', ClientCreateView.as_view(), name='send_contacts'),
    path('client_list', ClientListView.as_view(), name='client_list'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('messages_list', MessageListView.as_view(), name='messages_list'),
    path('message_create', MessageCreateView.as_view(), name='message_create'),
    path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('mailings_list', MailingListView.as_view(), name='mailings_list'),
    path('mailing_create', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing_log_list/', MailingLogListView.as_view(), name='mailing_log_list'),

]
