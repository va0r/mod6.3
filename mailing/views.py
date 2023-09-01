import random

from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from blog.models import Note
from mailing.forms import MailingSettingsForm, ClientForm, MessageForm
from mailing.models import MailingSettings, Client, MailingMessage, Contact


class StatisticsMixin:
    @staticmethod
    def get_statistics_context():
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


class BlogMixin:
    @staticmethod
    def get_blog_context():
        def select_random_notes():
            # Обновляем случайные числа в столбце random_number для всех записей
            for note in Note.objects.all():
                note.random_number = random.random()
                note.save()

            # Выбираем случайные записи, исключая дубликаты
            random_notes = Note.objects.filter(is_published=True).order_by('random_number')[:3]

            return random_notes

        selected_notes = select_random_notes()

        context = {
            'blog_1': selected_notes[0],
            'blog_2': selected_notes[1],
            'blog_3': selected_notes[2]
        }
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_context = self.get_blog_context()
        context.update(blog_context)
        return context


class CacheMixin:
    cache_timeout = 60 * 15  # 15 минут

    @classmethod
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        if settings.CACHE_ENABLED:
            return cache_page(cls.cache_timeout)(view)
        else:
            return view


class MailingSettingsListView(BlogMixin, StatisticsMixin, CacheMixin, ListView):
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


class MailingSettingsCreateView(BlogMixin, StatisticsMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')


class MailingSettingsUpdateView(BlogMixin, StatisticsMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')


class MailingSettingsDeleteView(BlogMixin, StatisticsMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:mailing_list')


class ClientListView(BlogMixin, StatisticsMixin, CacheMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Список клиентов'
    }


class ClientCreateView(BlogMixin, StatisticsMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')


class ClientUpdateView(BlogMixin, StatisticsMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')


class ClientDeleteView(BlogMixin, StatisticsMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients')


class MessageListView(BlogMixin, StatisticsMixin, CacheMixin, ListView):
    model = MailingMessage
    extra_context = {
        'title': 'Список сообщений'
    }


class MessageCreateView(BlogMixin, StatisticsMixin, CreateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')


class MessageUpdateView(BlogMixin, StatisticsMixin, UpdateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')


class MessageDeleteView(BlogMixin, StatisticsMixin, DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:messages')


class ContactListView(BlogMixin, StatisticsMixin, CacheMixin, ListView):
    model = Contact

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Контакты'
    }
