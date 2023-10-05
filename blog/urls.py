from django.urls import path

from blog.apps import BlogConfig
from blog.views import NoteCreateView, NoteListView, NoteDetailView, NoteUpdateView, NoteDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('create/', NoteCreateView.as_view(), name='CREATE'),
    path('', NoteListView.as_view(), name='READ_all'),
    path('read/<int:pk>/', NoteDetailView.as_view(), name='READ_one'),
    path('update/<int:pk>/', NoteUpdateView.as_view(), name='UPDATE'),
    path('delete/<int:pk>/', NoteDeleteView.as_view(), name='DELETE'),
]
