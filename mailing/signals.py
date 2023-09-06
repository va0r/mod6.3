from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.dispatch import receiver

from mailing.models import Client, MailingSettings


@receiver(post_save, sender=Client)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        # subject = 'Добро пожаловать!'
        # message = 'Добро пожаловать в наше приложение!'
        # from_email = settings.EMAIL_HOST_USER
        # recipient_list = [instance.email]
        # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        pass


@receiver(m2m_changed, sender=Client.groups.through)
def client_groups_changed(sender, instance, action, **kwargs):
    if action == 'post_add':
        groups_list = instance.groups.all()
        for group in groups_list:
            for ms in MailingSettings.objects.filter(groups=group,
                                                     status=MailingSettings.STATUS_STARTED):
                print(f'if_ {ms = }')
    elif action == 'post_remove':
        groups_list = instance.groups.all()
        for group in groups_list:
            for ms in MailingSettings.objects.filter(groups=group,
                                                     status=MailingSettings.STATUS_STARTED):
                print(f'elif_ {ms = }')
