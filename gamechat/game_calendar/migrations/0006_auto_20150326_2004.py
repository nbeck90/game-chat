# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_calendar', '0005_auto_20150326_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='creator',
            field=models.ForeignKey(related_name='created_events', to='profiles.Profile'),
            preserve_default=True,
        ),
    ]
