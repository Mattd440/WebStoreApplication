# Generated by Django 2.1.1 on 2018-10-18 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0007_card_default'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='billing_profile',
        ),
        migrations.DeleteModel(
            name='Card',
        ),
    ]
