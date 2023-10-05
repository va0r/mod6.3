from django.core.cache import cache
from django.http import HttpResponse


class CacheMixin:
    """
    Миксин-класс для кеширования контроллеров блога.
    """

    cache_timeout = 60 * 15  # Время жизни кеша в секундах (здесь 15 минут)

    def get_cache_key(self):
        """
        Генерация ключа для кеша на основе URL запроса.
        """
        return f'blog_{self.request.path}'

    def dispatch(self, request, *args, **kwargs):
        # Попробовать получить данные из кеша
        cached_data = cache.get(self.get_cache_key())

        if cached_data:
            # Если данные найдены в кеше, вернуть их
            return HttpResponse(cached_data)

        # Если данные не найдены в кеше, выполнить нормальный запрос
        response = super().dispatch(request, *args, **kwargs)

        # Рендерим только блок content перед сохранением в кеш
        if 'base.html' in response.template_name:
            content = response.rendered_content
        else:
            content = response.render()

        # Сохранить данные в кеш
        cache.set(self.get_cache_key(), content, self.cache_timeout)

        return response
