from django.contrib.auth.decorators import user_passes_test


def is_moderator(user):
    return user.groups.filter(name='Модераторы').exists()


moderator_required = user_passes_test(is_moderator)
