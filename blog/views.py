from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.forms import NoteForm
from blog.models import Note
from mailing.views import StatisticsMixin


class NoteCreateView(StatisticsMixin, CreateView):
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy('blog:READ_all')

    extra_context = {
        'title': 'Блог',
        'description': 'Создать запись'
    }

    def form_valid(self, form):
        if form.is_valid():
            new_note = form.save()
            new_note.slug = slugify(new_note.title)
            new_note.save()
        return super().form_valid(form)


class NoteListView(StatisticsMixin, ListView):
    model = Note

    extra_context = {
        'title': 'Блог',
        'description': 'Все записи'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class NoteDetailView(StatisticsMixin, DetailView):
    model = Note
    form_class = NoteForm

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        note_item = Note.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = 'Блог'
        context_data['description'] = f'Запись {note_item.title.title()}'
        context_data['full'] = True
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.cnt_views += 1
        self.object.save()
        return self.object


class NoteUpdateView(StatisticsMixin, UpdateView):
    model = Note
    form_class = NoteForm

    extra_context = {
        'title': 'Блог',
        'description': 'Редактировать запись'
    }

    def form_valid(self, form):
        if form.is_valid():
            new_note = form.save()
            new_note.slug = slugify(new_note.title)
            new_note.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:READ_one', args=[self.kwargs.get('pk')])


class NoteDeleteView(StatisticsMixin, DeleteView):
    model = Note
    success_url = reverse_lazy('blog:READ_all')
