from django.conf.urls import patterns, include, url

from meals import views

urlpatterns = patterns('',
    url(r'^$',
        views.MealsHomeView.as_view(),
        name='meals'
    ),
    url(r'^(?P<slug>[\w-]+)/$',
        views.MealView.as_view(),
        name='meal'
    ),
    url(r'^edit/(?P<slug>[\w-]+)/$',
        views.MealFormView.as_view(),
        name='meal-form'
    ),
    url(r'^tags/$',
        views.TagsHomeView.as_view(),
        name='tags'
    ),
    url(r'^tags/(?P<slug>[\w-]+)/$',
        views.TagView.as_view(),
        name='tag'
    ),
)
