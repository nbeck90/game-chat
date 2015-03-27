# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_calendar', '0008_event_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='date',
        ),
    ]
