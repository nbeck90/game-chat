# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0015_auto_20150402_0545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 2, 5, 51, 22, 646380, tzinfo=utc), blank=True),
            preserve_default=True,
        ),
    ]
