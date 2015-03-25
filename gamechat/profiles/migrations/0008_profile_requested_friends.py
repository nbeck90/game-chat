# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20150325_0005'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='requested_friends',
            field=models.ManyToManyField(related_name='_req_friend', null=True, to='profiles.Profile', blank=True),
            preserve_default=True,
        ),
    ]
