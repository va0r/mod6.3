import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.db import models

NULLABLE = {'blank': True, 'null': True}


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


def get_now_utc():
    return datetime.datetime.now().astimezone(datetime.timezone.utc)


class ClientGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название группы')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа клиентов'
        verbose_name_plural = 'Группы клиентов'
        ordering = ['pk']


class Client(models.Model):
    email = models.EmailField(verbose_name='Почта для рассылки')
    first_name = models.CharField(**NULLABLE, verbose_name='Имя', max_length=150)
    last_name = models.CharField(**NULLABLE, verbose_name='Фамилия', max_length=150)
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')
    is_blocked = models.BooleanField(verbose_name='Заблокирован', default=False)
    domain = models.CharField(verbose_name='Домен', max_length=255, blank=True, editable=False)

    groups = models.ManyToManyField(ClientGroup, related_name='clients', blank=True, verbose_name='Группы клиентов')

    def form_valid(self, form):
        # Создайте объект Client, но пока не сохраняйте его в базе данных
        client = form.save(commit=False)

        # Сохраните объект Client в базе данных
        client.save()

        # Если в форме были выбраны группы клиентов, добавьте их к объекту Client
        groups = form.cleaned_data['groups']
        for group in groups:
            client.groups.add(group)

        # Верните успешное перенаправление
        return super().form_valid(form)

    def save(self, *args, **kwargs):
        # запись домена почты в объект "Клиент"
        self.domain = self.email.split('@')[-1]
        # сохранение объекта
        super(Client, self).save(*args, **kwargs)

        # # отправка рассылок объекту
        # if not self.is_blocked:
        #     now_utc = get_now_utc()
        #     for ms in MailingSettings.objects.filter(status=MailingSettings.STATUS_STARTED):
        #         ml = MailingLog.objects.filter(client=self.id, settings=ms)
        #         if ml.exists():
        #             last_try_date_utc = ml.order_by('-last_try').first().last_try.astimezone(datetime.timezone.utc)
        #             if ms.period == MailingSettings.PERIOD_DAILY:
        #                 if (now_utc - last_try_date_utc).days >= 1:
        #                     send_email_one(ms, self)
        #             elif ms.period == MailingSettings.PERIOD_WEEKLY:
        #                 if (now_utc - last_try_date_utc).days >= 7:
        #                     send_email_one(ms, self)
        #             elif ms.period == MailingSettings.PERIOD_MONTHLY:
        #                 if (now_utc - last_try_date_utc).days >= 30:
        #                     send_email_one(ms, self)
        #         else:
        #             send_email_one(ms, self)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['pk']


class MailingSettings(models.Model):
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'
    PERIODS = (
        (PERIOD_DAILY, 'Ежедневная'),
        (PERIOD_WEEKLY, 'Раз в неделю'),
        (PERIOD_MONTHLY, 'Раз в месяц'),
    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'
    STATUSES = (
        (STATUS_STARTED, 'Запущена'),
        (STATUS_CREATED, 'Создана'),
        (STATUS_DONE, 'Завершена'),
    )

    time = models.TimeField(verbose_name='Время')
    period = models.CharField(max_length=20, choices=PERIODS, default=PERIOD_DAILY, verbose_name='Период')
    status = models.CharField(max_length=20, choices=STATUSES, default=STATUS_CREATED, verbose_name='Статус')
    message = models.ForeignKey('MailingMessage', on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)

    groups = models.ManyToManyField('ClientGroup', related_name='mailing_settings', blank=True,
                                    verbose_name='Группы рассылок')

    def form_valid(self, form):
        # Создайте объект MailingSettings, но пока не сохраняйте его в базе данных
        mailing_settings = form.save(commit=False)

        # Сохраните объект MailingSettings в базе данных
        mailing_settings.save()

        # Если в форме были выбраны группы, добавьте их к объекту MailingSettings
        groups = form.cleaned_data['groups']
        for group in groups:
            mailing_settings.groups.add(group)

        # Верните успешное перенаправление
        return super().form_valid(form)

    def save(self, *args, **kwargs):
        # сохранение объекта
        super(MailingSettings, self).save(*args, **kwargs)
        # # отправка рассылки объектам
        # if self.status == 'started':
        #     now_utc = get_now_utc()
        #     for mc in Client.objects.filter(is_blocked=False):
        #         ml = MailingLog.objects.filter(client=mc.id, settings=self)
        #         if ml.exists():
        #             last_try_date_utc = ml.order_by('-last_try').first().last_try.astimezone(datetime.timezone.utc)
        #             if self.period == MailingSettings.PERIOD_DAILY:
        #                 if (now_utc - last_try_date_utc).days >= 1:
        #                     send_email_one(self, mc)
        #             elif self.period == MailingSettings.PERIOD_WEEKLY:
        #                 if (now_utc - last_try_date_utc).days >= 7:
        #                     send_email_one(self, mc)
        #             elif self.period == MailingSettings.PERIOD_MONTHLY:
        #                 if (now_utc - last_try_date_utc).days >= 30:
        #                     send_email_one(self, mc)
        #         else:
        #             send_email_one(self, mc)

    def __str__(self):
        return f'{self.time} / {self.period}'

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'


class MailingMessage(models.Model):
    subject = models.CharField(max_length=250, verbose_name='Тема')
    message = models.TextField(verbose_name='Тело')

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'
        ordering = ['pk']


class MailingLog(models.Model):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'
    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Настройка')
    status = models.CharField(choices=STATUSES, default=STATUS_OK, verbose_name='Статус')
    last_try = models.DateTimeField(auto_now_add=True, verbose_name='Дата последней попытки')

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        ordering = ['pk']


class Contact(models.Model):
    key = models.CharField(max_length=25, verbose_name='Ключ')
    value = models.CharField(max_length=100, verbose_name='Значение')

    def __str__(self):
        return f'{self.key}: {self.value}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['pk']
