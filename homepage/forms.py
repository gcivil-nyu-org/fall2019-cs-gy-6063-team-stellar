from django import forms
from django.core.exceptions import ValidationError
from .models import ServiceType

class ServiceForm(forms.Form):
    # ServiceChoice = (
    #     ("Daily", "Daily"),
    #     ("Weekly", "Weekly"),
    #     ("Monthly", "Monthly"),
    # )
    #
    # # user_id = forms.IntegerField()
    # #
    # service = forms.ChoiceField(
    #     label="service",
    #     required= True,
    #     help_text="True",
    #     choices=ServiceChoice,
    #     widget=forms.Select(
    #         attrs={"class": "input100", "placeholder": "school", "autofocus": ""}
    #     ),
    # )
    service_type = forms.CharField(widget= forms.Select)
    #
    # def clean_service(self):
    #     data = self.cleaned_data['service']
    #     # Remember to always return the cleaned data.
    #     return data
    #
    class Meta:
        model = ServiceType
        fields = ['service_type']


class TypeOfServiceModalForm(forms.Form):
    serviceSelect = forms.CharField(widget=forms.Select)
    # service_type = forms.CharField(widget=forms.Select)

