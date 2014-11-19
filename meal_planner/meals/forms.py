from django import forms
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import InlineField, StrictButton

from meals.models import Meal

class MealHomeForm(forms.Form):

    NAME = 'name'
    RATING = 'rating'
    SORT_CHOICES = (
        (NAME, 'Name'),
        (RATING, 'Rating'),
    )

    sort_by = forms.ChoiceField(choices=SORT_CHOICES,
            label='Sort by', required=False)

class MealCreateForm(forms.ModelForm):

    class Meta:
        model = Meal
        fields = ['name', 'rating', 'url', 'description', 'tags']

    def __init__(self, *args, **kwargs):
        super(MealCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'meal-create-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.layout = Layout(
            'name',
            'rating',
            'url',
            'description',
            'tags',
             StrictButton('Add',
                 css_class='col-sm-offset-2 btn btn-default', type='submit'),
        )
        self.helper.form_action = reverse('meal-add')

class MealUpdateForm(forms.ModelForm):

    class Meta:
        model = Meal
        fields = ['rating', 'url', 'description', 'tags']

    def __init__(self, *args, **kwargs):
        super(MealUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'meal-update-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'
        self.helper.layout = Layout(
            'rating',
            'url',
            'description',
            'tags',
             StrictButton('Update',
                 css_class='col-sm-offset-2 btn btn-default', type='submit'),
        )
        self.helper.form_action = reverse('meal-update',
                args=[self.instance.slug])
