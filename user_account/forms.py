from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import LunchNinjaUser
import psycopg2
import csv
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class UserSignUpForm(UserCreationForm):

    SchoolChoice = (
        ("tandon school", "tandon school"),
        ("other school", "other school"),
    )
    DepartmentChoice = (
        ("Computer Science", "computer science"),
        ("other department", "other"),
    )
    username = forms.CharField(
        label="username",
        max_length=128,
        widget=forms.TextInput(
            attrs={"class": "input100", "placeholder": "Username", "autofocus": ""}
        ),
    )
    email = forms.EmailField(
        label="email",
        max_length=100,
        help_text="Required",
        widget=forms.TextInput(
            attrs={"class": "input100", "placeholder": "email", "autofocus": ""}
        ),
    )
    first_name = forms.CharField(
        label="FirstName",
        max_length=100,
        help_text="Required",
        widget=forms.TextInput(
            attrs={"class": "input100", "placeholder": "firstname", "autofocus": ""}
        ),
    )
    last_name = forms.CharField(
        label="LastName",
        max_length=100,
        help_text="Required",
        widget=forms.TextInput(
            attrs={"class": "input100", "placeholder": "lastname", "autofocus": ""}
        ),
    )
    Phone = forms.CharField(
        label="Phone",
        help_text="Optional",
        widget=forms.TextInput(
            attrs={"class": "input100", "placeholder": "phone", "autofocus": ""}
        ),
    )
    school = forms.ChoiceField(
        label="school",
        required=False,
        help_text="True",
        choices=SchoolChoice,
        widget=forms.Select(
            attrs={"class": "input100", "placeholder": "school", "autofocus": ""}
        ),
    )
    department = forms.ChoiceField(
        label="department",
        required=False,
        help_text="True",
        choices=DepartmentChoice,
        widget=forms.Select(
            attrs={"class": "input100", "placeholder": "department", "autofocus": ""}
        ),
    )
    password1 = forms.CharField(
        label="password1",
        max_length=256,
        widget=forms.PasswordInput(
            attrs={"class": "input100", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        label="password2",
        max_length=256,
        widget=forms.PasswordInput(
            attrs={"class": "input100", "placeholder": "Password Confirm"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        self.fields['school'] = forms.ChoiceField(
            choices=self.grabdata())

    def clean_Phone(self):

        # valid phone numbers US number only
        data = self.cleaned_data["Phone"]
        try:
            int(data)
            if not len(data) == 10:
                raise forms.ValidationError("Please enter a Valid Phone Number")
        except Exception:
            raise forms.ValidationError("Please enter a Valid Phone Number")
        return data

    def clean_email(self):
        data = self.cleaned_data["email"]
        domain = data.split("@")[1]
        if domain != "nyu.edu":
            raise forms.ValidationError("Please enter a NYU Email Address")
        return data

    def save(self, commit=True):
        user = super(UserSignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def grabschool(self):
        conn = psycopg2.connect(database="lunchninja", host="localhost");
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
        cur = conn.cursor()
        cur.execute('SELECT name  FROM school')
        count = cur.fetchall()
        # print(count)
        l = []
        for i in count:
            l.append((i[0],i[0]))
        # print(l)
        return l

    def grabdepartment(self, schoolid):
        conn = psycopg2.connect(database="lunchninja", host="localhost");
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
        cur = conn.cursor()
        cur.execute('SELECT name  FROM departmen')
        count = cur.fetchall()
        # print(count)
        l = []
        for i in count:
            l.append((i[0],i[0]))
        # print(l)
        return l


    class Meta:
        model = LunchNinjaUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "Phone",
            "school",
            "email",
            "password1",
            "password2",
        )


class UserSignInForm(forms.Form):
    username = forms.CharField(
        label="username",
        max_length=128,
        widget=forms.TextInput(
            attrs={"class": "input100", "placeholder": "Username", "autofocus": ""}
        ),
    )
    password = forms.CharField(
        label="password",
        max_length=256,
        widget=forms.PasswordInput(
            attrs={"class": "input100", "placeholder": "Password"}
        ),
    )

    class Meta:
        model = LunchNinjaUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "Phone",
            "school",
            "email",
            "password1",
            "password2",
        )

    # captcha = CaptchaField(label='verifycode')
