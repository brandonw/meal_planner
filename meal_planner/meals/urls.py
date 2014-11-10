from django.conf.urls import patterns, include, url

from meals import views

urlpatterns = patterns('',
    url(r'^$',
        views.MealsHomeView.as_view(),
        name='meals'
    ),
    url(r'^view/(?P<slug>[\w-]+)/$',
        views.MealView.as_view(),
        name='meal'
    ),
    url(r'^add/$',
        views.MealCreate.as_view(),
        name='meal-add'
    ),
    url(r'^edit/(?P<slug>[\w-]+)/$',
        views.MealUpdate.as_view(),
        name='meal-update'
    ),
    url(r'^delete/(?P<slug>[\w-]+)/$',
        views.MealDelete.as_view(),
        name='meal-delete'
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
