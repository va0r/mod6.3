from django.test import TestCase

from users.models import User


class UserModelTestCase(TestCase):
    def setUp(self):
        # Создаем тестового пользователя для каждого теста
        self.user = User.objects.create(email='test@example.com')
        self.user.set_password('password123')
        self.user.save()

    def test_user_creation(self):
        # Проверяем, что пользователь успешно создан
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('password123'))

    def test_str_method(self):
        # Проверяем, что метод __str__ возвращает правильное значение
        self.assertEqual(str(self.user), 'test@example.com')

    def test_verbose_name_plural(self):
        # Проверяем, что verbose_name_plural задан правильно
        self.assertEqual(str(User._meta.verbose_name_plural), 'Пользователи')

    def test_unique_email(self):
        # Проверяем, что поле email уникально
        duplicate_user = User(email='test@example.com')
        duplicate_user.set_password('anotherpassword')
        with self.assertRaises(Exception) as context:
            duplicate_user.save()
        self.assertIn('duplicate key value violates unique constraint', str(context.exception))
