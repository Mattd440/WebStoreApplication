# Generated by Django 2.1.1 on 2018-10-22 23:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0003_auto_20181022_2157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mailingpreference',
            old_name='msg',
            new_name='mailchimp_msg',
        ),
    ]