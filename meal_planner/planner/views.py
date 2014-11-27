from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
import datetime

from braces.views import LoginRequiredMixin
from planner.models import Day, DayRecipe
from planner.forms import PlannerHomeForm

class PlannerHomeView(LoginRequiredMixin, TemplateView):

    template_name = 'planner/planner_home.html'

    def get_context_data(self, **kwargs):
        context = super(PlannerHomeView, self).get_context_data(**kwargs)

        form = PlannerHomeForm(self.request.GET)
        form.is_valid()
        if 'date' in form.cleaned_data and form.cleaned_data['date'] is not None:
            start_date = form.cleaned_data['date']
        else:
            start_date = datetime.date.today()

        # always back up to first Sunday
        while start_date.weekday() is not 6:
            start_date = start_date - datetime.timedelta(1)

        end_date = start_date + datetime.timedelta(weeks=2)

        planned_recipes = DayRecipe.objects \
                .filter(recipe__user__username=self.request.user.username) \
                .filter(day__date__gte=start_date) \
                .filter(day__date__lt=end_date) \
                .order_by('day', 'meal')

        days = [start_date + datetime.timedelta(i) for i in range(14)]
        context['visible_recipes'] = \
            [(day, planned_recipes.filter(day__date=day)) for day in days]
        context['today'] = datetime.date.today()
        context['back'] = start_date - datetime.timedelta(7)
        context['forward'] = start_date + datetime.timedelta(7)

        return context
