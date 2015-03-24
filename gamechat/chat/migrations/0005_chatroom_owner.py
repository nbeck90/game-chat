# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20150324_2019'),
        ('chat', '0004_chatroom_subscribers'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='owner',
            field=models.OneToOneField(related_name='chat_room', default=None, to='profiles.Profile'),
            preserve_default=False,
        ),
    ]
