from django import forms
from django.core.urlresolvers import reverse

class PlannerHomeForm(forms.Form):

    date = forms.DateField(
            label='Date', required=False)

