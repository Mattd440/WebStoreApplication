# Generated by Django 2.1.1 on 2018-10-06 03:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20181006_0313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_total',
            new_name='total',
        ),
    ]
