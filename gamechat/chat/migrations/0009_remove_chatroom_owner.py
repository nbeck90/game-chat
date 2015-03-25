# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_auto_20150325_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='owner',
        ),
    ]
