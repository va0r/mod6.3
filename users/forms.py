from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.mail import send_mail

from mailing.forms import StyleFormMixin
from users.models import User


class StyledAuthenticationForm(StyleFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True, *args, **kwargs):
        user = super().save()
        send_mail(subject='Активация',
                  message=f'Для активации профиля пройдите по ссылке - http://127.0.0.1:8000/users/activate/{user.id}/',
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[user.email])
        user.is_active = False
        user.save()
        return user


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_active', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()

    is_active = forms.BooleanField(
        label='Активный',
        help_text='',
    )
