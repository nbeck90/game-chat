# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0014_auto_20150402_0501'),
        ('chat', '0010_chatroom_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(default=b'Type your info here')),
                ('date', models.DateTimeField()),
                ('room', models.ForeignKey(to='chat.ChatRoom')),
                ('user', models.ForeignKey(related_name='messages', to='profiles.Profile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
