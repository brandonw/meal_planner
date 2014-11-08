from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView

from braces.views import LoginRequiredMixin
from taggit.models import Tag
from .models import Meal

class MealsHomeView(LoginRequiredMixin, ListView):

    template_name = 'meals/meals_home.html'
    paginate_by = 10
    context_object_name = 'meals'

    def get_queryset(self):
        return Meal.objects \
                .order_by('name') \
                .filter(user__username=self.request.user.username)

class TagsHomeView(ListView):

    model = Tag

class MealView(DetailView):

    template_name = 'meals/meal.html'
    model = Meal
    context_object_name = 'meal'

    def get_context_data(self, **kwargs):
        context = super(MealView, self).get_context_data(**kwargs)
        context['rating_choices'] = Meal.RATING_CHOICES
        return context

class TagView(ListView):

    model = Meal

class MealFormView(FormView):

    pass
