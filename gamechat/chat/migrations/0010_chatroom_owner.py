# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20150325_0005'),
        ('chat', '0009_remove_chatroom_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='owner',
            field=models.OneToOneField(related_name='chat_room', null=True, blank=True, to='profiles.Profile'),
            preserve_default=True,
        ),
    ]
