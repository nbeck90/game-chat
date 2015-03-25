# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_chatroom_main_room'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='main_room',
        ),
        migrations.AddField(
            model_name='chatroom',
            name='main',
            field=models.CharField(default=b'halo', max_length=200),
            preserve_default=True,
        ),
    ]
