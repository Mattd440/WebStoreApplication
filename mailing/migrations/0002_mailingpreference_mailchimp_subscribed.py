# Generated by Django 2.1.1 on 2018-10-22 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailingpreference',
            name='mailchimp_subscribed',
            field=models.NullBooleanField(),
        ),
    ]