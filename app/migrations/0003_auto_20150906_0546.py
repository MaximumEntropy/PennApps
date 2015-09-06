# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150906_0534'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialogueblock',
            name='end_time',
            field=models.FloatField(default=0, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dialogueblock',
            name='start_time',
            field=models.FloatField(default=0, db_index=True),
            preserve_default=False,
        ),
    ]
