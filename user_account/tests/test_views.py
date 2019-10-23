from django.test import TestCase


import mock


class SignupViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):

        response = self.client.get("/signup/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get("/signup/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")

    # def test_call_view_fails_blank(self):
    # 	response = self.client.post('/signup/', {})
    # 	self.assertFormError(response, 'form', 'email', 'This field is required.')
    # 	self.assertFormError(response, 'form', 'username', 'This field is required.')
    # 	self.assertFormError(response, 'form', 'password1', 'This field is required.')
    # 	self.assertFormError(response, 'form', 'password2', 'This field is required.')

    def test_call_view_success_correct_fields(self):
        signupObj = {
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
        response = self.client.post("/signup/", signupObj)
        self.assertContains(
            response,
            "We have sent you an email, please confirm your email address to complete registration",
        )


class LoginViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")


class LogoutViewTest(TestCase):
    def test_logout_without_user_session(self):
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)


class ValidateViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/activate/Mw/5aq-2e4c9f14af4a0758633b/")
        self.assertEqual(response.status_code, 200)

    def test_invalid_activation_link(self):
        response = self.client.get("/activate/Mw/5aq-2e4c9f14af4a0758633b/")
        self.assertContains(response, "Activation link is invalid")

    def check_token(user, token):
        return True

    def get_user_obj(**kargs):
        class userObj:
            def __init__(self):
                self.is_active = True

            def save(self):
                return "Saved"

        return userObj()

    @mock.patch("user_account.views.login")
    @mock.patch(
        "user_account.views.LunchNinjaUser.objects.get", side_effect=get_user_obj
    )
    @mock.patch(
        "user_account.token_generator.account_activation_token.check_token",
        side_effect=check_token,
    )
    def test_valid_activation_link(self, mock_token_generator, mock_user, mock_login):
        response = self.client.get("/activate/Mw/5aq-2e4c9f14af4a0758633b/")
        self.assertContains(response, "Your account has been activate successfully")
