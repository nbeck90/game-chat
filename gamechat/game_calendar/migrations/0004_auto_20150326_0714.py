# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20150325_1649'),
        ('game_calendar', '0003_auto_20150326_0516'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='attending',
            field=models.ManyToManyField(related_name='accepted_invites', null=True, to='profiles.Profile', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='invitees',
            field=models.ManyToManyField(related_name='invited_to', null=True, to='profiles.Profile', blank=True),
            preserve_default=True,
        ),
    ]
