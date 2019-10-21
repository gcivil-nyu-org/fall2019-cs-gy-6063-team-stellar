from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class UserSignUpForm(UserCreationForm):
    username = forms.CharField(label="username", max_length=128,
                               widget=forms.TextInput(attrs={'class': "input100", 'placeholder': "Username", 'autofocus': ''}))
    email = forms.EmailField(label="email",max_length=100,help_text='Required',
                             widget=forms.TextInput(attrs={'class': "input100", 'placeholder': "email",'autofocus': ''}))
    first_name = forms.CharField(label="FirstName",max_length=100, help_text='Required',
                                 widget=forms.TextInput(attrs={'class': "input100", 'placeholder': "firstname",'autofocus': ''}))
    last_name = forms.CharField(label="LastName",max_length=100, help_text='Required',
                                widget=forms.TextInput(attrs={'class': "input100", 'placeholder': "lastname",'autofocus': ''}))
    Phone = forms.CharField(label="Phone",max_length=100, help_text='Optional',
                            widget=forms.TextInput(attrs={'class': "input100", 'placeholder': "phone",'autofocus': ''}))
    school = forms.CharField(label="school",max_length=100, required=False, help_text='True',
                             widget=forms.TextInput(attrs={'class': "input100", 'placeholder': "school",'autofocus': ''}))
    department = forms.CharField(label="department", max_length=100, required=False, help_text='True',
                             widget=forms.TextInput(attrs={'class': "input100", 'placeholder': "department", 'autofocus': ''}))
    password1 = forms.CharField(label="password1", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': "input100", 'placeholder': "Password"}))
    password2 = forms.CharField(label="password2", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': "input100", 'placeholder': "Password Confirm"}))
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
        fields = ('username', 'first_name', 'last_name', 'Phone', 'school', 'email', 'password1', 'password2')
class UserSignInForm(forms.Form):
    username = forms.CharField(label="username", max_length=128,widget=forms.TextInput(attrs={'class': "input100", 'placeholder': "Username",'autofocus': ''}))
    password = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': "input100",'placeholder': "Password"}))
    # captcha = CaptchaField(label='verifycode')

