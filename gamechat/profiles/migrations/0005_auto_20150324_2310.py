# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20150324_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default=b'gamechat/static/link.jpg', null=True, upload_to=b'gamechat/static', blank=True),
            preserve_default=True,
        ),
    ]
