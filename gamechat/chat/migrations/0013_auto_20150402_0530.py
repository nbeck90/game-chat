# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0012_auto_20150402_0527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='description',
        ),
        migrations.AddField(
            model_name='message',
            name='text',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
