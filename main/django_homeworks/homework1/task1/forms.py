from django import forms
from django.core.exceptions import ValidationError

from .models import Department


class CompareForm(forms.Form):

    choice_one = forms.ChoiceField()
    choice_two = forms.ChoiceField()

    number_staff = forms.BooleanField(required=False)
    sum_prices_of_sold_items = forms.BooleanField(required=False)
    sum_prices_of_unsold_items = forms.BooleanField(required=False)
    sum_prices_of_all_items = forms.BooleanField(required=False)
    number_prices_of_sold_items = forms.BooleanField(required=False)
    number_prices_of_unsold_items = forms.BooleanField(required=False)
    number_prices_of_all_items = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['choice_one'].choices = \
            [(department.id, str(department))
             for department in Department.objects.all()]

        self.fields['choice_two'].choices = \
            [(department.id, str(department))
             for department in Department.objects.all()]

    def clean(self):

        if self.cleaned_data.get("choice_one") == self.cleaned_data.get("choice_two"):
            raise ValidationError({'choice_two': ["second department cannot be equal to first!"]})

        return self.cleaned_data
