import random

from django.http import Http404

from blog.models import Note
from mailing.models import MailingSettings, Client


class StatisticsMixin:
    @staticmethod
    def get_statistics_context(user):
        if not user.is_authenticated:
            context = {
                'count_mailings_all': 0,
                'count_mailings_active': 0,
                'count_clients': 0,
            }
        elif user.groups.filter(name='Модераторы').exists():
            context = {
                'count_mailings_all': MailingSettings.objects.count(),
                'count_mailings_active': MailingSettings.objects.filter(status=MailingSettings.STATUS_STARTED).count(),
                'count_clients': Client.objects.distinct().count(),
            }
        else:
            context = {
                'count_mailings_all': MailingSettings.objects.filter(owner=user).count(),
                'count_mailings_active': MailingSettings.objects.filter(owner=user, status=MailingSettings.STATUS_STARTED).count(),
                'count_clients': Client.objects.filter(owner=user).distinct().count(),
            }
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        statistics_context = self.get_statistics_context(user)

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

        user = self.request.user
        if user.groups.filter(name='Модераторы').exists():
            return self.model.objects.all()
        else:
            return self.model.objects.filter(owner=user)


class RequestFormMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class FormValidMixin:
    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)
