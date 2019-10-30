from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import LunchNinjaUser
from homepage.models import UserRequest, Department, School, Cuisine


#
# def retrieveschool():
#     conn = psycopg2.connect(database="lunchninja", host="localhost", user='postgres', password='password')
#     # conn = psycopg2.connect(database="lunchninja", host="localhost")
#     conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#     cur = conn.cursor()
#     cur.execute("SELECT name,id  FROM school")
#     count = cur.fetchall()
#     conn.commit()
#     conn.close()
#     return count
#
#
# def retrievedepartment():
#     conn = psycopg2.connect(database="lunchninja", host="localhost", user='postgres', password='password')
#     # conn = psycopg2.connect(database="lunchninja", host="localhost")
#     conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#     cur = conn.cursor()
#     sqlline = "SELECT name,school FROM department"
#     cur.execute(sqlline)
#     count = cur.fetchall()
#     conn.commit()
#     conn.close()
#     return count


def creat_school_tuple():

    read_school = School.objects.all()
    schoollist = []
    # read_school = retrieveschool()
    for s in read_school:
        schoollist.append((s.name, s.name))
    schoollist[0] = ("select school", "select school")
    return tuple(schoollist)


def creat_department_tuple():
    read_department = Department.objects.all()

    departmentlist = []
    # read_department = retrievedepartment()
    for d in read_department:
        departmentlist.append((d.name, d.name))
    departmentlist[0] = ("select department", "select department")
    return tuple(departmentlist)


class UserSignUpForm(UserCreationForm):
    SchoolChoice = creat_school_tuple()
    DepartmentChoice = creat_department_tuple()
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
