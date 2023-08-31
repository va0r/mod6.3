from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Note(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.CharField(max_length=250, **NULLABLE, verbose_name='Slug')
    content = models.TextField(max_length=1000, verbose_name='Содержание')
    image = models.ImageField(upload_to='blog/', **NULLABLE, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    cnt_views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ('pk',)
