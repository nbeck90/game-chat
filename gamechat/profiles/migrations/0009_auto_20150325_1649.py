# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_profile_requested_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='blocking',
            field=models.ManyToManyField(related_name='blocked_by', null=True, to='profiles.Profile', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='requested_friends',
            field=models.ManyToManyField(related_name='requesting_friend', null=True, to='profiles.Profile', blank=True),
            preserve_default=True,
        ),
    ]
