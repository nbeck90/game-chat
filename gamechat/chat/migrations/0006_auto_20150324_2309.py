# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_chatroom_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='owner',
            field=models.OneToOneField(related_name='chat_room', null=True, blank=True, to='profiles.Profile'),
            preserve_default=True,
        ),
    ]
