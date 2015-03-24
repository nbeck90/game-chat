# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20150324_1607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='subscribers',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
