from django import forms

from blog.models import Note
from mailing.forms import StyleFormMixin


class NoteForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'content', 'image', 'is_published')
