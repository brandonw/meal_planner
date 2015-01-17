from django.conf.urls import patterns, url

from recipes import views

urlpatterns = patterns(
    '',
    url(r'^$',
        views.RecipesHomeView.as_view(),
        name='recipes'
        ),
    url(r'^view/(?P<slug>[\w-]+)/$',
        views.RecipeView.as_view(),
        name='recipe'
        ),
    url(r'^add/$',
        views.RecipeCreateView.as_view(),
        name='recipe-add'
        ),
    url(r'^edit/(?P<slug>[\w-]+)/$',
        views.RecipeUpdateView.as_view(),
        name='recipe-update'
        ),
    url(r'^rate/(?P<slug>[\w-]+)/(?P<rating>[0-5])/$',
        views.RecipeUpdateRatingView.as_view(),
        name='recipe-update-rating'
        ),
    url(r'^delete/(?P<slug>[\w-]+)/$',
        views.RecipeDeleteView.as_view(),
        name='recipe-delete'
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
