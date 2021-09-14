# Generated by Django 3.2.7 on 2021-09-10 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFriend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('udpated_date', models.DateTimeField(auto_now=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'New'), (1, 'Active'), (2, 'Rejected')])),
                ('source_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='source_user', to=settings.AUTH_USER_MODEL)),
                ('target_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='target_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
