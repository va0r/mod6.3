from django.core.management import BaseCommand

from mailing.services import send_mail_all


class Command(BaseCommand):

    def handle(self, *args, **options):
        send_mail_all()
