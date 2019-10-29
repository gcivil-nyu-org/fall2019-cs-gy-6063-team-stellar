from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import LunchNinjaUser
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import csv

def grabschool():
    conn = psycopg2.connect(database="lunchninja", host="localhost", user='postgres', password='123456')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("SELECT name  FROM school")
    count = cur.fetchall()
    # print(count)
    schoollist = []
    for i in count:
        schoollist.append((i[0], i[0]))
    # print(l)
    return tuple(schoollist)

def grabdepartment():
    conn = psycopg2.connect(database="lunchninja", host="localhost", user='postgres', password='123456')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()
    cur.execute("SELECT name  FROM department")
    count = cur.fetchall()
    # print(count)
    departmentlist = []
    for i in count:
        departmentlist.append((i[0], i[0]))


    return tuple(departmentlist)

def creat_school_tuple(school_csv):
    with open(school_csv,'r',encoding='utf-8') as in_f1:
        read_school = csv.reader(in_f1)
        schoollist=[]
        for s in read_school:
            schoollist.append((s[0],s[0]))
        schoollist[0]=('select school','select school')
        return tuple(schoollist)
def creat_department_tuple(department_csv):
    with open(department_csv,'r',encoding='utf-8') as in_f1:
        read_department = csv.reader(in_f1)
        departmentlist=[]
        for s in read_department:
            departmentlist.append((s[0],s[0]))
        departmentlist[0]=('select department','select department')
        return tuple(departmentlist)
class UserSignUpForm(UserCreationForm):

    SchoolChoice = creat_school_tuple('datasource\\School.csv')
    print(SchoolChoice)
    DepartmentChoice = creat_department_tuple('datasource\\Department.csv')
    print(DepartmentChoice)

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
        # print(self.grabschool())
        # self.fields["school"] = forms.ChoiceField(choices=self.grabschool())

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
