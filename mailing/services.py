import datetime

from django.conf import settings
from django.core.mail import send_mail

from mailing.models import MailingLog, MailingSettings, Client


def send_email_one(ms, mc):
    result = send_mail(
        subject=ms.message.subject,
        message=ms.message.message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[mc.email],
        fail_silently=False
    )

    MailingLog.objects.create(
        status=MailingLog.STATUS_OK if result else MailingLog.STATUS_FAILED,
        settings=ms,
        client=mc
    )


def send_mail_all():
    now = datetime.datetime.now()
    now_utc = now.astimezone(datetime.timezone.utc)
    for ms in MailingSettings.objects.filter(status=MailingSettings.STATUS_STARTED):
        for mc in Client.objects.filter(is_blocked=False):
            ml = MailingLog.objects.filter(client=mc.id, settings=ms)
            if ml.exists():
                last_try_date = ml.order_by('-last_try').first()
                last_try_date_utc = last_try_date.last_try.astimezone(datetime.timezone.utc)
                if ms.period == MailingSettings.PERIOD_DAILY:
                    if (now_utc - last_try_date_utc).days >= 1:
                        send_email_one(ms, mc)
                elif ms.period == MailingSettings.PERIOD_WEEKLY:
                    if (now_utc - last_try_date_utc).days >= 7:
                        send_email_one(ms, mc)
                elif ms.period == MailingSettings.PERIOD_MONTHLY:
                    if (now_utc - last_try_date_utc).days >= 30:
                        send_email_one(ms, mc)
            else:
                send_email_one(ms, mc)
