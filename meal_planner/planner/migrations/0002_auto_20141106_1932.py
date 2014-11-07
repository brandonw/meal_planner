# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0002_meal_description'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('planner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DayMeal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveSmallIntegerField()),
                ('day', models.ForeignKey(to='planner.Day')),
                ('meal', models.ForeignKey(to='meals.Meal')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='dayplan',
            name='meals',
        ),
        migrations.RemoveField(
            model_name='dayplan',
            name='user',
        ),
        migrations.DeleteModel(
            name='DayPlan',
        ),
        migrations.AddField(
            model_name='day',
            name='meals',
            field=models.ManyToManyField(to='meals.Meal', through='planner.DayMeal'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='day',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
