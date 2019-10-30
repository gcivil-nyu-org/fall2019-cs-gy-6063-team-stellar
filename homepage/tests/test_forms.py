from django.test import TestCase
from homepage.forms import TypeOfServiceModalForm


class UserSignUpFormTest(TestCase):
    def test_serviceSelect_label(self):
        form = TypeOfServiceModalForm()
        self.assertTrue(form.fields["serviceSelect"].label is None)

    def test_form_valid(self):
        data = {"serviceSelect": "weekly"}
        form = TypeOfServiceModalForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_not_valid(self):
        data = {"serviceSelect": 12324}
        form = TypeOfServiceModalForm(data=data)
        self.assertFalse(not form.is_valid())
