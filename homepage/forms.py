from django import forms
from django.core.exceptions import ValidationError
from .models import ServiceType, UserRequest


class ServiceForm(forms.Form):
    service_type = forms.CharField(widget=forms.Select)
    #
    # def clean_service(self):
    #     data = self.cleaned_data['service']
    #     # Remember to always return the cleaned data.
    #     return data
    #
    class Meta:
        model = ServiceType
        fields = ["service_type"]


class TypeOfServiceModalForm(forms.Form):
    serviceSelect = forms.CharField(widget=forms.Select)

    class Meta:
        model = UserRequest
        fields = ["service_type"]

    def save(self, commit=True):
        form = super(TypeOfServiceModalForm, self).save(commit=False)
        form.service_type = self.serviceSelect
        if commit:
            form.save()
        return form


class SchoolModalForm(forms.Form):
    school = forms.CharField(widget=forms.Select)
    department = forms.CharField(widget=forms.Select)

    class Meta:
        model = UserRequest
        fields = ["school", "department"]

    def save(self, commit=True):
        form = super(SchoolModalForm, self).save(commit=False)
        form.school = self.school
        form.department = self.department
        if commit:
            form.save()
        return form


class CuisineModalForm(forms.Form):
    cuisine = forms.CharField(widget=forms.Select)

    class Meta:
        model = UserRequest
        fields = ["cuisine"]

    def save(self, commit=True):
        form = super(CuisineModalForm, self).save(commit=False)
        form.school = self.school
        form.department = self.department
        if commit:
            form.save()
        return form
