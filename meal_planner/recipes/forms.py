from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import StrictButton

from recipes.models import Recipe


class RecipeHomeForm(forms.Form):

    NAME = 'name'
    RATING = 'rating'
    SORT_CHOICES = (
        (NAME, 'Name'),
        (RATING, 'Rating'),
    )

    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        label='Sort by', required=False)


class RecipeCreateForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['name', 'rating', 'url', 'description', 'tags']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RecipeCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'recipe-create-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.layout = Layout(
            'name',
            'rating',
            'url',
            'description',
            'tags',
            StrictButton(
                'Add',
                css_class='col-sm-offset-2 btn btn-default', type='submit'),
        )
        self.helper.form_action = reverse('recipe-add')

    def clean(self):
        cleaned_data = super(RecipeCreateForm, self).clean()
        name = cleaned_data.get('name')

        if name and Recipe.objects \
                .filter(user=self.user) \
                .filter(name=name) \
                .exists():
            raise forms.ValidationError('%s recipe already exists.' % name)


class RecipeUpdateForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['rating', 'url', 'description', 'tags']

    def __init__(self, *args, **kwargs):
        super(RecipeUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'recipe-update-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.layout = Layout(
            'rating',
            'url',
            'description',
            'tags',
            StrictButton(
                'Update',
                css_class='col-sm-offset-2 btn btn-default', type='submit'),
        )
        self.helper.form_action = reverse(
            'recipe-update',
            args=[self.instance.slug])


class RecipeUpdateRatingForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['rating']
