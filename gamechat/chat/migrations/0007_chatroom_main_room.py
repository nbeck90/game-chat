# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_auto_20150324_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='main_room',
            field=models.CharField(default=b'SSB', max_length=200),
            preserve_default=True,
        ),
    ]
