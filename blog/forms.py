from django import forms

from blog.models import Note


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        """
        Стилизация формы
        """

        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class NoteForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'content', 'image', 'is_published')
