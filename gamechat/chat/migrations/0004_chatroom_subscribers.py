# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20150323_2055'),
        ('chat', '0003_auto_20150324_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='subscribers',
            field=models.ManyToManyField(related_name='subs', to='profiles.Profile'),
            preserve_default=True,
        ),
    ]
