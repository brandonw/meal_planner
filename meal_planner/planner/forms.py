from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import StrictButton

from planner.models import DayRecipe
from recipes.models import Recipe


class RedirectToDateForm(forms.Form):
    date = forms.DateField()


class DayRecipeCreateForm(forms.ModelForm):
    recipe = forms.ModelChoiceField(
        queryset=Recipe.objects.all(),
        empty_label=None)

    class Meta:
        model = DayRecipe
        fields = ['recipe']

    def __init__(self, *args, **kwargs):
        self.date = kwargs.pop('date', None)
        self.meal = kwargs.pop('meal', 0)
        user = kwargs.pop('user', None)
        super(DayRecipeCreateForm, self).__init__(*args, **kwargs)
        self.fields['recipe'].queryset = Recipe.objects.filter(
            user__username=user)
        self.helper = FormHelper()
        self.helper.form_id = 'dayrecipe-create-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.layout = Layout(
            'recipe',
            StrictButton(
                'Add',
                css_class='col-sm-offset-2 btn btn-default', type='submit'),
        )
        self.helper.form_action = reverse(
            'create-dayrecipe',
            kwargs={
                'year': self.date.year,
                'month': self.date.month,
                'day': self.date.day,
                'meal': self.meal
            })
