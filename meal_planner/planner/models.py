from django.db import models
from meals.models import Meal

class Day(models.Model):

    date = models.DateField()
    user = models.ForeignKey('users.User')
    meals = models.ManyToManyField('meals.Meal', through='DayMeal')

    def __unicode__(self):
        return self.date.isoformat()

class DayMeal(models.Model):

    day = models.ForeignKey(Day)
    meal = models.ForeignKey(Meal)
    order = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.day.date.isoformat() + ' - ' + self.meal.__unicode__()
