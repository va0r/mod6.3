from django.contrib.auth import get_user_model
from django.db import models

NULLABLE = {'blank': True, 'null': True}
User = get_user_model()


class ClientGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название группы')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_groups', verbose_name='Владелец',
                              **NULLABLE)

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

    groups = models.ManyToManyField(ClientGroup, related_name='clients', blank=True, verbose_name='Группы клиентов',
                                    default=None)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients', verbose_name='Владелец',
                              **NULLABLE)

    def save(self, *args, **kwargs):
        self.domain = self.email.split('@')[-1]
        super(Client, self).save(*args, **kwargs)

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

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mailing_settings', verbose_name='Владелец',
                              **NULLABLE)

    def __str__(self):
        return f'{self.time} / {self.period}'

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'


class MailingMessage(models.Model):
    subject = models.CharField(max_length=250, verbose_name='Тема')
    message = models.TextField(verbose_name='Тело')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mailing_message', verbose_name='Владелец',
                              **NULLABLE)

    def __str__(self):
        return self.subject

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

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['pk']
