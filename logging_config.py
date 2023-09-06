import logging

# Определите формат журналирования
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Определите настройки журналирования
logging.basicConfig(level=logging.INFO, format=log_format)

# Подключитесь к журналу Celery
celery_logger = logging.getLogger('celery')
celery_logger.setLevel(logging.WARNING)
