from django import forms

from .models import UserRequest
from bootstrap_modal_forms.forms import BSModalForm

class ServiceForm(BSModalForm):
    ServiceChoice = (
        ("Daily", "Daily"),
        ("Weekly", "Weekly"),
        ("Monthly", "Monthly"),
    )

    service_type = service = forms.ChoiceField(
        label="service",
        required=False,
        help_text="True",
        choices=ServiceChoice,
        widget=forms.Select(
            attrs={"class": "input100", "placeholder": "school", "autofocus": ""}
        ),
    )
    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserRequest
        exclude = ['user_id', 'timestamp', 'exp_time', 'cuisine']



class SchoolForm(BSModalForm):
    SchoolChoice = (
        ("tandon school", "tandon school"),
        ("other school", "other school"),
    )

    DepartmentChoice = (
        ("Computer Science", "computer science"),
        ("other department", "other"),
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

    class Meta:
        model = UserRequest
        exclude = ['school', 'department']


# class UserRequestForm(BSModalForm):
#     ServiceChoice = (
#         ("Daily", "Daily"),
#         ("Weekly", "Weekly"),
#         ("Monthly", "Monthly"),
#     )
#
#     SchoolChoice = (
#         ("tandon school", "tandon school"),
#         ("other school", "other school"),
#     )
#
#     DepartmentChoice = (
#         ("Computer Science", "computer science"),
#         ("other department", "other"),
#     )
#
#     CuisineChoice = (
#         ("Computer Science", "computer science"),
#         ("other department", "other"),
#     )
#
#     service = forms.ChoiceField(
#         label="school",
#         required=False,
#         help_text="True",
#         choices=SchoolChoice,
#         widget=forms.Select(
#             attrs={"class": "input100", "placeholder": "school", "autofocus": ""}
#         ),
#     )
#
#     school = forms.ChoiceField(
#         label="school",
#         required=False,
#         help_text="True",
#         choices=SchoolChoice,
#         widget=forms.Select(
#             attrs={"class": "input100", "placeholder": "school", "autofocus": ""}
#         ),
#     )
#
#     department = forms.ChoiceField(
#         label="department",
#         required=False,
#         help_text="True",
#         choices=DepartmentChoice,
#         widget=forms.Select(
#             attrs={"class": "input100", "placeholder": "department", "autofocus": ""}
#         ),
#     )
#
#     cuisine = forms.ChoiceField(
#         label="cuisine",
#         required=False,
#         help_text="True",
#         choices=CuisineChoice,
#         widget=forms.Select(
#             attrs={"class": "input100", "placeholder": "department", "autofocus": ""}
#         ),
#     )
#
#
#
#     def clean_email(self):
#         data = self.cleaned_data["email"]
#         domain = data.split("@")[1]
#         if domain != "nyu.edu":
#             raise forms.ValidationError("Please enter a NYU Email Address")
#         return data
#
#     def save(self, commit=True):
#         user = super(UserRequestForm, self).save(commit=False)
#         user.email = self.cleaned_data["email"]
#         if commit:
#             user.save()
#         return user
#
#     class Meta:
#         model = UserRequest
#         fields = (
#             "service",
#             "school",
#             "department",
#             "cuisine"
#         )
