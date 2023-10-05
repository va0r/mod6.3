from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from mailing.models import Client, ClientGroup, MailingSettings, MailingMessage


class Command(BaseCommand):

    def handle(self, *args, **options):
        admin_user = get_user_model().objects.get(email="admin@admin.admin")

        Client.objects.update(owner=admin_user)
        ClientGroup.objects.update(owner=admin_user)
        MailingSettings.objects.update(owner=admin_user)
        MailingMessage.objects.update(owner=admin_user)
