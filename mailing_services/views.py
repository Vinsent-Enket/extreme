from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from mailing_services.models import Client, Message, Mailing, MailingLogs

from mailing_services.tools.mailing_tool import MessageService, send_mailing
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def contacts(request):
    return render(request, 'mailing_services/contacts.html')


# Create your views here.
class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ('email', 'name', 'comments',)
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        if form.is_valid():
            new_client = form.save()
            new_client.slug = slugify(new_client.name)
            new_client.save()
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing_services/client_list.html'


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ('email', 'name', 'comments',)
    success_url = reverse_lazy('catalog:index')

    def get_success_url(self):
        return reverse_lazy('mailing_services:client_list')

    def form_valid(self, form):
        if form.is_valid():
            new_client = form.save()
            new_client.slug = slugify(new_client.name)
            new_client.save()
            print(new_client.name)
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing_services:client_list')


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ('header', 'body',)
    success_url = reverse_lazy('mailing_services:messages_list')

    def form_valid(self, form):
        if form.is_valid():
            new_message = form.save()
            new_message.save()
            return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing_services/messages_list.html'


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('header', 'body',)
    success_url = reverse_lazy('mailing_services:message_list')

    def form_valid(self, form):
        if form.is_valid():
            new_message = form.save()
            new_message.save()
            return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing_services:message_list')


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    fields = ('time', 'regularity', 'client', 'message')
    success_url = reverse_lazy('mailing_services:mailings_list')

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.user = self.request.user
        mailing.status = 'created'
        mailing.save()

        message_service = MessageService(mailing)
        send_mailing(mailing)
        # sender()
        message_service.create_task()
        mailing.status = 'in_work'
        mailing.save()

        return super(MailingCreateView, self).form_valid(form)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing_services/mailings_list.html'


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    success_url = reverse_lazy('mailing_services:mailings_list')
    model = Mailing

    fields = ('time', 'regularity', 'client', 'message')

    def form_valid(self, form):
        if form.is_valid():
            new_mail = form.save()
            new_mail.save()

        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing_services:mailings_list')


class MailingLogListView(LoginRequiredMixin, ListView):
    """Представление для просмотра всех попыток рассылок"""
    model = MailingLogs
    template_name = 'mailing_services/mailinglog_list.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = "Попытки рассылки"
    #     context['log_list'] = MailingLogs.objects.all()
    #     return context
