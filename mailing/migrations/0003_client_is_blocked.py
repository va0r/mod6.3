# Generated by Django 4.2.4 on 2023-08-30 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_mailingsettings_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='is_blocked',
            field=models.BooleanField(default=False, verbose_name='Заблокирован'),
        ),
    ]
