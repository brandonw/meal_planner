from django.conf.urls import patterns, include, url

from planner import views

urlpatterns = patterns('',
    url(r'^$',
        views.PlannerHomeView.as_view(),
        name='planner'
    ),
)
