# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0003_auto_20141106_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='rating',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, b'Not rated'), (1, b'Awful'), (2, b'Bad'), (3, b'Average'), (4, b'Good'), (5, b'Great')]),
        ),
    ]
