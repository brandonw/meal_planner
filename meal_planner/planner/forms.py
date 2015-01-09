from django import forms


class RedirectToDateForm(forms.Form):
    date = forms.DateField()
