from django.apps import AppConfig


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'
    verbose_name = 'Рассылка'

    def ready(self):
        import mailing.signals
        print(f'\n>>>>>>>>>> {mailing.signals.get_now_utc() = } <<<<<<<<<<\n')
