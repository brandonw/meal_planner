from django.db import models
from django.core.urlresolvers import reverse
from autoslug import AutoSlugField
from taggit.managers import TaggableManager


class Recipe(models.Model):
    NOT_RATED = 0
    AWFUL = 1
    BAD = 2
    AVERAGE = 3
    GOOD = 4
    GREAT = 5
    RATING_CHOICES = (
        (NOT_RATED, 'Not rated'),
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
                                              default=NOT_RATED)

    url = models.URLField(blank=True)
    description = models.TextField(blank=True)

    tags = TaggableManager()

    class Meta:
        unique_together = (('user', 'name'),)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipe', self.slug)
