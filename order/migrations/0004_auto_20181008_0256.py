# Generated by Django 2.1.1 on 2018-10-08 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20181006_0338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, default='abc', max_length=120, unique=True),
        ),
    ]