from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required')
    
    def clean_email(self):
        data = self.cleaned_data['email']
        domain = data.split('@')[1]
        if domain != "nyu.edu":
            raise forms.ValidationError("Please enter a NYU Email Address")
        return data
    
    def save(self, commit=True):
        user = super(UserSignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

