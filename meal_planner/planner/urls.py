from django.conf.urls import patterns, url

from planner import views

urlpatterns = patterns(
    '',
    url(r'^$',
        views.PlannerHomeView.as_view(),
        name='planner'
        ),
    url(r'^(?P<year>[\d]+)/(?P<month>[\d]+)/(?P<day>[\d]+)/$',
        views.PlannerDayView.as_view(),
        name='planner-day'
        ),
    url(r'^redirect-to-date/$',
        views.RedirectToDateView.as_view(),
        name='redirect-to-date'
        ),
    url(r'^delete/(?P<pk>[\d]+)/$',
        views.DayRecipeDeleteView.as_view(),
        name='delete-dayrecipe'
        ),
    url(r'^(?P<year>[\d]+)/(?P<month>[\d]+)/' +
        '(?P<day>[\d]+)/add/(?P<meal>[\d])/$',
        views.DayRecipeCreateView.as_view(),
        name='create-dayrecipe'
        ),
)
