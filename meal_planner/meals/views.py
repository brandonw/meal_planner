from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView,\
        FormMixin
from django.contrib.messages.views import SuccessMessageMixin

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

class MealView(LoginRequiredMixin, DetailView):

    template_name = 'meals/meal.html'
    model = Meal
    context_object_name = 'meal'

    def get_queryset(self):
        return Meal.objects \
                .filter(user__username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super(MealView, self).get_context_data(**kwargs)
        context['rating_choices'] = Meal.RATING_CHOICES
        return context

class MealCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    template_name = 'meals/meal_create.html'
    model = Meal
    fields = ['name', 'rating', 'url', 'description', 'tags']

    def get_queryset(self):
        return Meal.objects \
                .filter(user__username=self.request.user.username)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(MealCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('meals')

    def get_success_message(self, cleaned_data):
        return u'{0} created!'.format(self.object)

class MealUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    template_name = 'meals/meal_update.html'
    model = Meal
    fields = ['rating', 'url', 'description', 'tags']

    def get_queryset(self):
        return Meal.objects \
                .filter(user__username=self.request.user.username)

    def get_success_url(self):
        return reverse('meals')

    def get_success_message(self, cleaned_data):
        return u'{0} updated!'.format(self.object)

class MealDelete(LoginRequiredMixin, DeleteView):

    template_name = 'meals/meal_delete.html'
    model = Meal

    def get_queryset(self):
        return Meal.objects \
                .filter(user__username=self.request.user.username)

class TagsHomeView(LoginRequiredMixin, ListView):

    model = Tag

class TagView(LoginRequiredMixin, ListView):

    model = Meal

