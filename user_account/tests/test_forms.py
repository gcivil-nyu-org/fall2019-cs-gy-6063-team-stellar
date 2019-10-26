from django.test import TestCase
from user_account.forms import UserSignUpForm, UserSignInForm


class UserSignUpFormTest(TestCase):
    def test_email_label(self):
        form = UserSignUpForm()
        self.assertTrue(
            form.fields["email"].label is None or form.fields["email"].label == "email"
        )

    # def test_email_text(self):
    # 	form = UserSignUpForm()
    # 	self.assertEqual(form.fields['email'].help_text, 'Required(NYU Email ID)')

    def test_email_is_nyu(self):
        data = {
            "username": "testUser",
            "email": "up@nyu.edu",
            "first_name": "donald",
            "last_name": "trump",
            "Phone": "1234567890",
            "school": "other school",
            "department": "other department",
            "password1": "Pass12345",
            "password2": "Pass12345",
        }
        form = UserSignUpForm(data=data)
        self.assertTrue(form.is_valid())

    def test_email_is_not_nyu(self):
        data = {
            "username": "testUser",
            "email": "up@usc.edu",
            "first_name": "donald",
            "last_name": "trump",
            "Phone": "1234567890",
            "school": "other school",
            "department": "other department",
            "password1": "Pass12345",
            "password2": "Pass12345",
        }
        form = UserSignUpForm(data=data)
        self.assertFalse(form.is_valid())


class UserSignInFormTest(TestCase):
    def test_username(self):
        form = UserSignInForm()
        self.assertTrue(form.fields["username"].label == "username")
        self.assertTrue(form.fields["username"].max_length == 128)

    def test_password(self):
        form = UserSignInForm()
        self.assertTrue(form.fields["password"].label == "password")
        self.assertTrue(form.fields["password"].max_length == 256)

    # def test_captcha_label(self):
    # 	form = UserSignInForm()
    # 	self.assertTrue(form.fields['captcha'].label == 'verifycode')
