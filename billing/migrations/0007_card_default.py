# Generated by Django 2.1.1 on 2018-10-18 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0006_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='default',
            field=models.BooleanField(default=True),
        ),
    ]
