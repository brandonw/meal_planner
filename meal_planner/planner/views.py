from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin

from braces.views import LoginRequiredMixin
from planner.models import Day, DayMeal

class PlannerHomeView(LoginRequiredMixin, TemplateView):

    template_name = 'planner/planner_home.html'

    def get_context_data(self, **kwargs):
        context = super(PlannerHomeView, self).get_context_data(**kwargs)
        planned_meals = DayMeal.objects \
                .filter(meal__user__username=self.request.user.username)
        return context
