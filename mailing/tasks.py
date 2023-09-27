from celery import shared_task

from mailing.services import send_mail_all


@shared_task
def send_mail_task():
    send_mail_all()
