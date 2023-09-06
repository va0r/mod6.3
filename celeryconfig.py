from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# Установите переменную окружения DJANGO_SETTINGS_MODULE, чтобы Celery знал, какую конфигурацию Django использовать
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('skychimp')

# Загрузите настройки Celery из объекта settings.py вашего Django проекта
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически найдите и зарегистрируйте задачи из приложения "mailing"
app.autodiscover_tasks(['mailing'])
