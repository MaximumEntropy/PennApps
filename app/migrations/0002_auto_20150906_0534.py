# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='speaker',
            name='conversation',
        ),
        migrations.AddField(
            model_name='conversation',
            name='duration',
            field=models.IntegerField(default=0, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dialogueblock',
            name='speaker',
            field=models.TextField(),
        ),
        migrations.DeleteModel(
            name='Speaker',
        ),
    ]
