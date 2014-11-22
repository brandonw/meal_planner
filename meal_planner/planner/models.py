from django.db import models
from recipes.models import Recipe

class Day(models.Model):

    date = models.DateField()
    user = models.ForeignKey('users.User')
    recipes = models.ManyToManyField('recipes.Recipe', through='DayRecipe')

    def __unicode__(self):
        return self.date.isoformat()

class DayRecipe(models.Model):

    BREAKFAST = 0
    LUNCH     = 1
    DINNER    = 2
    MEAL_CHOICES = (
        (BREAKFAST, 'Breakfast'),
        (LUNCH, 'Lunch'),
        (DINNER, 'Dinner'),
    )

    day = models.ForeignKey(Day)
    recipe = models.ForeignKey(Recipe)
    meal = models.PositiveSmallIntegerField(choices=MEAL_CHOICES,
                                            default=DINNER)

    def __unicode__(self):
        return self.day.date.isoformat() + ' - ' + self.recipe.__unicode__()
