# Generated by Django 2.1.1 on 2018-10-15 01:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('analytics', '0003_usersession'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectViewed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('ip_address', models.CharField(blank=True, max_length=120, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Object Viewed',
                'verbose_name_plural': 'Objects Viewed',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.RemoveField(
            model_name='productviewed',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='productviewed',
            name='user',
        ),
        migrations.DeleteModel(
            name='ProductViewed',
        ),
    ]
