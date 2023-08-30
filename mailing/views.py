from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mailing.forms import MailingSettingsForm, ClientForm, MessageForm
from mailing.models import MailingSettings, Client, MailingMessage, Contact


class StatisticsMixin:
    def get_statistics_context(self):
        context = {
            'count_mailings_all': MailingSettings.objects.all().count(),
            'count_mailings_active': MailingSettings.objects.filter(status=MailingSettings.STATUS_STARTED).count(),
            'count_clients': Client.objects.distinct().count(),
        }
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        statistics_context = self.get_statistics_context()
        context.update(statistics_context)
        return context


class MailingSettingsListView(StatisticsMixin, ListView):
    model = MailingSettings

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Email Рассылка'
        context_data['description'] = 'Главная'
        return context_data


def toggle__is_blocked(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if not client.is_blocked:
        client.is_blocked = True
    else:
        client.is_blocked = False
    client.save()

    return redirect('mailing:clients')


class MailingSettingsCreateView(StatisticsMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')


class MailingSettingsUpdateView(StatisticsMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')


class MailingSettingsDeleteView(StatisticsMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:mailing_list')


class ClientListView(StatisticsMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Список клиентов'
    }


class ClientCreateView(StatisticsMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')


class ClientUpdateView(StatisticsMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')


class ClientDeleteView(StatisticsMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients')


class MessageListView(StatisticsMixin, ListView):
    model = MailingMessage
    extra_context = {
        'title': 'Список сообщений'
    }


class MessageCreateView(StatisticsMixin, CreateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')


class MessageUpdateView(StatisticsMixin, UpdateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')


class MessageDeleteView(StatisticsMixin, DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:messages')


class ContactListView(StatisticsMixin, ListView):
    model = Contact

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Контакты'
    }
