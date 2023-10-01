from django import forms

from mailing.models import MailingSettings, Client, MailingMessage, ClientGroup


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        """
        Стилизация формы
        """

        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        exclude = ('owner',)


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)


class ClientGroupForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = ClientGroup
        exclude = ('owner',)


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingMessage
        exclude = ('owner',)
