from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView, RedirectView
import datetime

from braces.views import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from planner.models import DayRecipe
from planner.forms import RedirectToDateForm


class PlannerHomeView(LoginRequiredMixin, RedirectView):

    permanent = False
    query_string = False
    pattern_name = 'planner-day'

    def get_redirect_url(self, *args, **kwargs):
        start_date = datetime.date.today()
        kwargs['year'] = start_date.year
        kwargs['month'] = start_date.month
        kwargs['day'] = start_date.day
        return super(PlannerHomeView, self).get_redirect_url(*args, **kwargs)


class PlannerDayView(LoginRequiredMixin, TemplateView):

    template_name = 'planner/planner_day.html'

    def get_context_data(self, **kwargs):
        context = super(PlannerDayView, self).get_context_data(**kwargs)
        year = int(kwargs['year'])
        month = int(kwargs['month'])
        day = int(kwargs['day'])
        selected = datetime.date(year, month, day)
        start = selected
        prev_week = selected - datetime.timedelta(weeks=1)
        next_week = selected + datetime.timedelta(weeks=1)
        while start.weekday() is not 6:
            start = start - datetime.timedelta(1)
        end = selected + datetime.timedelta(weeks=1)
        day_recipes = DayRecipe.objects \
            .filter(recipe__user__username=self.request.user.username) \
            .filter(day__date__gte=start) \
            .filter(day__date__lte=end) \
            .select_related('day', 'recipe') \
            .order_by('day', 'meal', 'pk')

        # group all recipes by the day they are planned for
        days_dict = {}
        for day_recipe in day_recipes:
            if day_recipe.day.date not in days_dict:
                days_dict[day_recipe.day.date] = []
            days_dict[day_recipe.day.date].append(day_recipe)

        days = []
        for offset in range(8):
            date = start + datetime.timedelta(offset)
            days.append((date, self.get_summary(days_dict, date)))
            if date == selected:
                context['todays_recipes'] = self.get_detail(days_dict, date)

        context['days'] = days
        context['selected'] = selected
        context['yesterday'] = selected - datetime.timedelta(1)
        context['tomorrow'] = selected + datetime.timedelta(1)
        context['prev_week'] = prev_week
        context['next_week'] = next_week
        return context

    def get_summary(self, days, date):
        if date not in days:
            return (0, 0, 0)
        day_recipes = days[date]
        breakfasts = 0
        lunches = 0
        dinners = 0
        for dr in day_recipes:
            if dr.meal == DayRecipe.BREAKFAST:
                breakfasts += 1
            elif dr.meal == DayRecipe.LUNCH:
                lunches += 1
            elif dr.meal == DayRecipe.DINNER:
                dinners += 1

        return (breakfasts, lunches, dinners)

    def get_detail(self, days, date):
        if date not in days:
            return ([], [], [])
        day_recipes = days[date]
        breakfasts = []
        lunches = []
        dinners = []
        for dr in day_recipes:
            if dr.meal == DayRecipe.BREAKFAST:
                breakfasts.append(dr)
            elif dr.meal == DayRecipe.LUNCH:
                lunches.append(dr)
            elif dr.meal == DayRecipe.DINNER:
                dinners.append(dr)

        return (breakfasts, lunches, dinners)


class RedirectToDateView(LoginRequiredMixin, RedirectView):

    permanent = False
    query_string = False
    pattern_name = 'planner-day'

    def get_redirect_url(self, *args, **kwargs):
        form = RedirectToDateForm(self.request.GET)
        date = datetime.date.today()
        if form.is_valid():
            date = form.cleaned_data['date']

        kwargs['year'] = date.year
        kwargs['month'] = date.month
        kwargs['day'] = date.day
        return super(RedirectToDateView, self).get_redirect_url(
            *args, **kwargs)


class DayRecipeDeleteView(LoginRequiredMixin, DeleteView):

    def get_queryset(self):
        return DayRecipe.objects \
            .filter(day__user__username=self.request.user.username)

    def get_object(self, queryset=None):
        dayrecipe = super(DayRecipeDeleteView, self).get_object(queryset)
        self.date = dayrecipe.day.date
        return dayrecipe

    def get_success_url(self):
        return reverse(
            'planner-day',
            kwargs={
                'year': self.date.year,
                'month': self.date.month,
                'day': self.date.day
                })
