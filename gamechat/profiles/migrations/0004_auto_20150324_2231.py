# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20150324_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='chat_room_name',
            field=models.CharField(max_length=64, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default=b'profiles/static/link.jpg', null=True, upload_to=b'profiles/static', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='slug',
            field=models.CharField(unique=True, max_length=32, blank=True),
            preserve_default=True,
        ),
    ]
