from django.db import models
from autoslug import AutoSlugField
from taggit.managers import TaggableManager

class Meal(models.Model):
    NOT_EDIBLE = 0
    AWFUL      = 1
    BAD        = 2
    AVERAGE    = 3
    GOOD       = 4
    GREAT      = 5
    RATING_CHOICES = (
        (NOT_EDIBLE, 'Not edible'),
        (AWFUL, 'Awful'),
        (BAD, 'Bad'),
        (AVERAGE, 'Average'),
        (GOOD, 'Good'),
        (GREAT, 'Great'),
    )

    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique_with='user')
    user = models.ForeignKey('users.User')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES,
                                              null=True,
                                              default=NOT_EDIBLE)

    url = models.URLField(blank=True)
    description = models.TextField(blank=True)

    tags = TaggableManager()

    def __unicode__(self):
        return self.name
