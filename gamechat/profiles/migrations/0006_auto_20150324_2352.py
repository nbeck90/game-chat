# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20150324_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default=b'photots/link.jpg', null=True, upload_to=b'photos/', blank=True),
            preserve_default=True,
        ),
    ]
