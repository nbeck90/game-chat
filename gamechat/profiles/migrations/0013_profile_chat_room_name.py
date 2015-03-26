# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_remove_profile_chat_room_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='chat_room_name',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
    ]
