# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='recipe',
            unique_together=set([('user', 'name')]),
        ),
    ]
