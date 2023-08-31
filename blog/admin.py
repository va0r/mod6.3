from django.contrib import admin

from blog.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'content', 'created_at', 'is_published', 'cnt_views', )
    list_filter = ('title', )
    search_fields = ('title', 'content', )
