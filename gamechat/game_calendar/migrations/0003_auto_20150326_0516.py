# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20150325_1649'),
        ('game_calendar', '0002_event'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.AddField(
            model_name='event',
            name='creator',
            field=models.ForeignKey(default=None, to='profiles.Profile'),
            preserve_default=False,
        ),
    ]
