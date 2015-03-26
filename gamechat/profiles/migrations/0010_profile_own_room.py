# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20150325_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='own_room',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
