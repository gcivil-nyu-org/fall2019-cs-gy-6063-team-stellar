from django import forms


class TypeOfServiceModalForm(forms.Form):
    serviceSelect = forms.CharField(widget=forms.Select)
