import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.dispatch import receiver

from mailing.models import Client, MailingSettings, get_now_utc, MailingLog, send_email_one, ClientGroup


@receiver(post_save, sender=Client)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Добро пожаловать!'
        message = 'Добро пожаловать в наше приложение!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)


@receiver(m2m_changed, sender=Client.groups.through)
def client_groups_changed(sender, instance, action, **kwargs):
    groups_list = []
    is_blocked__content = True
    if action == 'post_add':
        groups_list = instance.groups.all()
        is_blocked__content = instance.is_blocked
    elif action == 'post_remove':
        groups_list = instance.groups.all()
        is_blocked__content = instance.is_blocked

    conditions = [
        len(groups_list) > 0,
        not is_blocked__content
    ]

    if all(conditions):
        now_utc = get_now_utc()
        for group in groups_list:
            for ms in MailingSettings.objects.filter(groups=group, status=MailingSettings.STATUS_STARTED):
                ml = MailingLog.objects.filter(client=instance.id, settings=ms)
                if ml.exists():
                    last_try_date_utc = ml.order_by('-last_try').first().last_try.astimezone(datetime.timezone.utc)
                    if ms.period == MailingSettings.PERIOD_DAILY:
                        if (now_utc - last_try_date_utc).days >= 1:
                            send_email_one(ms, instance)
                    elif ms.period == MailingSettings.PERIOD_WEEKLY:
                        if (now_utc - last_try_date_utc).days >= 7:
                            send_email_one(ms, instance)
                    elif ms.period == MailingSettings.PERIOD_MONTHLY:
                        if (now_utc - last_try_date_utc).days >= 30:
                            send_email_one(ms, instance)
                else:
                    send_email_one(ms, instance)


@receiver(m2m_changed, sender=MailingSettings.groups.through)
def mailing_settings_groups_changed(sender, instance, action, **kwargs):
    groups_list = []
    message_content = ''
    status_content = ''
    if action == 'post_add':
        groups_list = instance.groups.all()
        message_content = instance.message
        status_content = instance.status
    elif action == 'post_remove':
        groups_list = instance.groups.all()
        message_content = instance.message
        status_content = instance.status

    conditions = [
        len(groups_list) > 0,
        message_content is not None,
        status_content == 'started'
    ]

    if all(conditions):
        now_utc = get_now_utc()
        for group in groups_list:
            group_object = ClientGroup.objects.get(name=group)
            clients_in_group = Client.objects.filter(groups=group_object)
            if not clients_in_group.exists():
                return
            for mc in clients_in_group:
                ml = MailingLog.objects.filter(client=mc, settings=instance)
                if ml.exists():
                    last_try_date_utc = ml.order_by('-last_try').first().last_try.astimezone(datetime.timezone.utc)
                    if instance.period == MailingSettings.PERIOD_DAILY:
                        if (now_utc - last_try_date_utc).days >= 1:
                            send_email_one(instance, mc)
                    elif instance.period == MailingSettings.PERIOD_WEEKLY:
                        if (now_utc - last_try_date_utc).days >= 7:
                            send_email_one(instance, mc)
                    elif instance.period == MailingSettings.PERIOD_MONTHLY:
                        if (now_utc - last_try_date_utc).days >= 30:
                            send_email_one(instance, mc)
                else:
                    send_email_one(instance, mc)
