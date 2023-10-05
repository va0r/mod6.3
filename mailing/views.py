from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mailing.forms import MailingSettingsForm, ClientForm, MessageForm, ClientGroupForm, MailingSettingsModeratorForm, \
    ClientModeratorForm
from mailing.mixins import BlogMixin, StatisticsMixin, QuerysetMixin, RequestFormMixin, AccessCheckMixin, FormValidMixin
from mailing.models import MailingSettings, Client, MailingMessage, Contact, ClientGroup
from mailing.permissions import moderator_required, is_moderator


class MailingSettingsListView(LoginRequiredMixin, BlogMixin, StatisticsMixin, QuerysetMixin, ListView):
    model = MailingSettings

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Email Рассылка'
        context_data['description'] = 'Главная'
        context_data['is_moderator'] = self.request.user.groups.filter(name='Модераторы').exists()
        return context_data


@login_required
@moderator_required
def toggle__is_blocked(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if not client.is_blocked:
        client.is_blocked = True
    else:
        client.is_blocked = False
    client.save()

    return redirect('mailing:clients')


class MailingSettingsCreateView(LoginRequiredMixin, BlogMixin, StatisticsMixin, RequestFormMixin, FormValidMixin,
                                CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Добавление настроек рассылки'
    }


class MailingSettingsUpdateView(LoginRequiredMixin, BlogMixin, StatisticsMixin, AccessCheckMixin, RequestFormMixin,
                                UpdateView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:mailing_list')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Изменение настроек рассылки'
    }

    def dispatch(self, *args, **kwargs):
        if is_moderator(self.request.user):
            self.form_class = MailingSettingsModeratorForm
        else:
            self.form_class = MailingSettingsForm
        return super().dispatch(*args, **kwargs)


class MailingSettingsDeleteView(LoginRequiredMixin, BlogMixin, StatisticsMixin, AccessCheckMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:mailing_list')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Удаление настроек рассылки'
    }


class ClientListView(LoginRequiredMixin, BlogMixin, StatisticsMixin, QuerysetMixin, ListView):
    model = Client

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Email Рассылка'
        context_data['description'] = 'Список клиентов'
        context_data['is_moderator'] = self.request.user.groups.filter(name='Модераторы').exists()
        return context_data


class ClientCreateView(LoginRequiredMixin, BlogMixin, StatisticsMixin, RequestFormMixin, FormValidMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Добавление клиента рассылки'
    }


class ClientUpdateView(LoginRequiredMixin, BlogMixin, StatisticsMixin, AccessCheckMixin, RequestFormMixin, UpdateView):
    model = Client
    success_url = reverse_lazy('mailing:clients')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Изменение клиента рассылки'
    }

    def dispatch(self, *args, **kwargs):
        if is_moderator(self.request.user):
            self.form_class = ClientModeratorForm
        else:
            self.form_class = ClientForm
        return super().dispatch(*args, **kwargs)


class ClientDeleteView(LoginRequiredMixin, BlogMixin, StatisticsMixin, AccessCheckMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Удаление клиента рассылки'
    }


class MessageListView(LoginRequiredMixin, BlogMixin, StatisticsMixin, QuerysetMixin, ListView):
    model = MailingMessage

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Email Рассылка'
        context_data['description'] = 'Список сообщений'
        context_data['is_moderator'] = self.request.user.groups.filter(name='Модераторы').exists()
        return context_data


class MessageCreateView(LoginRequiredMixin, BlogMixin, StatisticsMixin, FormValidMixin, CreateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Добавление сообщения для рассылки'
    }


class MessageUpdateView(LoginRequiredMixin, BlogMixin, StatisticsMixin, AccessCheckMixin, UpdateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Изменение сообщения для рассылки'
    }


class MessageDeleteView(LoginRequiredMixin, BlogMixin, StatisticsMixin, AccessCheckMixin, DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:messages')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Удаление сообщения для рассылки'
    }


class ContactListView(BlogMixin, StatisticsMixin, ListView):
    model = Contact

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Контакты'
    }


class ClientGroupListView(LoginRequiredMixin, BlogMixin, StatisticsMixin, QuerysetMixin, ListView):
    model = ClientGroup

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Email Рассылка'
        context_data['description'] = 'Список групп клиентов'
        context_data['is_moderator'] = self.request.user.groups.filter(name='Модераторы').exists()
        return context_data


class ClientGroupCreateView(LoginRequiredMixin, BlogMixin, StatisticsMixin, FormValidMixin, CreateView):
    model = ClientGroup
    form_class = ClientGroupForm
    success_url = reverse_lazy('mailing:groups')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Добавление списка групп клиентов'
    }


class ClientGroupUpdateView(LoginRequiredMixin, BlogMixin, StatisticsMixin, AccessCheckMixin, UpdateView):
    model = ClientGroup
    form_class = ClientGroupForm
    success_url = reverse_lazy('mailing:groups')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Изменение списка групп клиентов'
    }


class ClientGroupDeleteView(LoginRequiredMixin, BlogMixin, StatisticsMixin, AccessCheckMixin, DeleteView):
    model = ClientGroup
    success_url = reverse_lazy('mailing:groups')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Удаление списка групп клиентов'
    }
