from django.test import TestCase

from blog.models import Note


class NoteModelTest(TestCase):

    def test_note_creation(self):
        """
        Проверка создания записи (Note).
        """
        note = Note.objects.create(
            title="Заголовок записи",
            content="Содержание записи",
            is_published=True,
        )
        self.assertEqual(note.title, "Заголовок записи")
        self.assertEqual(note.content, "Содержание записи")
        self.assertTrue(note.is_published)

    def test_random_number_generation(self):
        """
        Проверка генерации случайного числа при сохранении записи.
        """
        note = Note.objects.create(
            title="Заголовок записи",
            content="Содержание записи",
            is_published=True,
        )
        self.assertIsNotNone(note.random_number)

    def test_str_representation(self):
        """
        Проверка строкового представления записи.
        """
        note = Note.objects.create(
            title="Заголовок записи",
            content="Содержание записи",
            is_published=True,
        )
        self.assertEqual(str(note), "Заголовок записи")

    def test_default_values(self):
        """
        Проверка значений по умолчанию для полей модели.
        """
        note = Note.objects.create(
            title="Заголовок записи",
            content="Содержание записи",
        )
        # Проверяем, что поле image не имеет файла
        self.assertFalse(note.image)
        self.assertEqual(note.cnt_views, 0)
        self.assertIsNotNone(note.created_at)
