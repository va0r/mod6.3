from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.filter(email='admin@admin.admin').first()

        user.set_password('ghjcnjq77')
        user.save()
