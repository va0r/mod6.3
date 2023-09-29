import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, request
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from blog.models import Note
from mailing.forms import MailingSettingsForm, ClientForm, MessageForm, ClientGroupForm
from mailing.models import MailingSettings, Client, MailingMessage, Contact, ClientGroup


class StatisticsMixin:
    @staticmethod
    def get_statistics_context(user):
        context = {
            'count_mailings_all': MailingSettings.objects.filter(owner=user).count(),
            'count_mailings_active': MailingSettings.objects.filter(owner=user, status=MailingSettings.STATUS_STARTED).count(),
            'count_clients': Client.objects.filter(owner=user).distinct().count(),
        }
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            statistics_context = self.get_statistics_context(user)
        else:
            statistics_context = self.get_statistics_context(None)

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


class AccessCheckMixin:
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class QuerysetMixin:
    model = None

    def get_queryset(self):
        if self.model is None:
            raise ValueError("The 'model' attribute must be defined in the subclass.")
        return self.model.objects.filter(owner=self.request.user)


class MailingSettingsListView(LoginRequiredMixin, BlogMixin, StatisticsMixin, QuerysetMixin, ListView):
    model = MailingSettings

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Email Рассылка'
        context_data['description'] = 'Главная'
        return context_data


@login_required
def toggle__is_blocked(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if not client.is_blocked:
        client.is_blocked = True
    else:
        client.is_blocked = False
    client.save()

    return redirect('mailing:clients')


class MailingSettingsCreateView(LoginRequiredMixin, BlogMixin, StatisticsMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Добавление настроек рассылки'
    }

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingSettingsUpdateView(LoginRequiredMixin, BlogMixin, StatisticsMixin, AccessCheckMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Изменение настроек рассылки'
    }


class MailingSettingsDeleteView(LoginRequiredMixin, BlogMixin, StatisticsMixin, AccessCheckMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:mailing_list')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Удаление настроек рассылки'
    }


class ClientListView(LoginRequiredMixin, BlogMixin, StatisticsMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Список клиентов'
    }


class ClientCreateView(LoginRequiredMixin, BlogMixin, StatisticsMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Добавление клиента рассылки'
    }

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, BlogMixin, StatisticsMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Изменение клиента рассылки'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class ClientDeleteView(LoginRequiredMixin, BlogMixin, StatisticsMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Удаление клиента рассылки'
    }


class MessageListView(LoginRequiredMixin, BlogMixin, StatisticsMixin, ListView):
    model = MailingMessage

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Список сообщений'
    }


class MessageCreateView(LoginRequiredMixin, BlogMixin, StatisticsMixin, CreateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Добавление сообщения для рассылки'
    }

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, BlogMixin, StatisticsMixin, UpdateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Изменение сообщения для рассылки'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class MessageDeleteView(LoginRequiredMixin, BlogMixin, StatisticsMixin, DeleteView):
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


class ClientGroupListView(LoginRequiredMixin, BlogMixin, StatisticsMixin, ListView):
    model = ClientGroup
    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Список групп клиентов'
    }


class ClientGroupCreateView(LoginRequiredMixin, BlogMixin, StatisticsMixin, CreateView):
    model = ClientGroup
    form_class = ClientGroupForm
    success_url = reverse_lazy('mailing:groups')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Добавление списка групп клиентов'
    }

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientGroupUpdateView(LoginRequiredMixin, BlogMixin, StatisticsMixin, UpdateView):
    model = ClientGroup
    form_class = ClientGroupForm
    success_url = reverse_lazy('mailing:groups')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Изменение списка групп клиентов'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class ClientGroupDeleteView(LoginRequiredMixin, BlogMixin, StatisticsMixin, DeleteView):
    model = ClientGroup
    success_url = reverse_lazy('mailing:groups')

    extra_context = {
        'title': 'Email Рассылка',
        'description': 'Удаление списка групп клиентов'
    }
