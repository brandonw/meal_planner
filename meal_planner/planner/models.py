from django.db import models

class DayPlan(models.Model):

    date = models.DateField()
    user = models.ForeignKey('users.User')
    meals = models.ManyToManyField('meals.Meal')
    order = models.PositiveSmallIntegerField()
