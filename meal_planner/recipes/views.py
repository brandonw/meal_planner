from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from braces.views import LoginRequiredMixin
from taggit.models import Tag
from recipes.models import Recipe
from recipes.forms import RecipeHomeForm, RecipeCreateForm, RecipeUpdateForm


class RecipesHomeView(LoginRequiredMixin, ListView):

    template_name = 'recipes/recipes_home.html'
    paginate_by = 10
    context_object_name = 'recipes'

    def get_queryset(self):
        self.form = RecipeHomeForm(self.request.GET)
        self.form.is_valid()
        if ('sort_by' in self.form.cleaned_data and
                self.form.cleaned_data['sort_by'] == RecipeHomeForm.RATING):
            return Recipe.objects \
                .order_by('-rating', 'name') \
                .filter(user__username=self.request.user.username)
        else:
            return Recipe.objects \
                .order_by('name', '-rating') \
                .filter(user__username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super(RecipesHomeView, self).get_context_data(**kwargs)
        context['sort_choices'] = RecipeHomeForm.SORT_CHOICES
        sort_by = self.form.cleaned_data['sort_by']
        if sort_by == '':
            sort_by = RecipeHomeForm.SORT_CHOICES[0][0]
        context['sort_by'] = sort_by
        return context


class RecipeView(LoginRequiredMixin, DetailView):

    template_name = 'recipes/recipe.html'
    model = Recipe
    context_object_name = 'recipe'

    def get_queryset(self):
        return Recipe.objects \
            .filter(user__username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super(RecipeView, self).get_context_data(**kwargs)
        context['rating_choices'] = Recipe.RATING_CHOICES
        return context


class RecipeCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    template_name = 'recipes/recipe_create.html'
    form_class = RecipeCreateForm

    def get_queryset(self):
        return Recipe.objects \
            .filter(user__username=self.request.user.username)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(RecipeCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('recipes')

    def get_success_message(self, cleaned_data):
        return u'{0} created!'.format(self.object)


class RecipeUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    template_name = 'recipes/recipe_update.html'
    form_class = RecipeUpdateForm

    def get_queryset(self):
        return Recipe.objects \
            .filter(user__username=self.request.user.username)

    def get_success_url(self):
        return reverse('recipes')

    def get_success_message(self, cleaned_data):
        return u'{0} updated!'.format(self.object)


class RecipeDelete(LoginRequiredMixin, DeleteView):

    template_name = 'recipes/recipe_delete.html'
    model = Recipe

    def get_queryset(self):
        return Recipe.objects \
            .filter(user__username=self.request.user.username)

    def get_success_url(self):
        return reverse('recipes')


class TagsHomeView(LoginRequiredMixin, ListView):

    model = Tag


class TagView(LoginRequiredMixin, ListView):

    model = Recipe

