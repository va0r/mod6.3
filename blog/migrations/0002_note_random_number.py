# Generated by Django 4.2.4 on 2023-08-31 12:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='random_number',
            field=models.FloatField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
    ]
