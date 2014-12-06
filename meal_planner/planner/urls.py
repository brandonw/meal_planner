from django.conf.urls import patterns, include, url

from planner import views

urlpatterns = patterns('',
    url(r'^$',
        views.PlannerHomeView.as_view(),
        name='planner'
    ),
    url(r'^(?P<year>[\d-]+)/(?P<month>[\d-]+)/(?P<day>[\d-]+)/$',
        views.PlannerDayView.as_view(),
        name='planner-day'
    ),
)
