from django.test import TestCase
from unittest import mock


class UserserviceViewTest(TestCase):
    def is_authenticated(self):
        return True

    def User_request_Obj(**kargs):
        class cuisine_for_mock:
            def __init__(self):
                pass

            def clear(**kargs):
                return "Cleared"

            def add(**kargs):
                return "Added"

        class userObj:
            def __init__(self):
                self.service_type = 'Monthly'
                self.school = 'Tandon School of Engineering'
                self.cuisines = cuisine_for_mock

            def save(self):
                return "Saved"

        return userObj()
    def send_email_mock(self,p2,p3):
        pass
    @mock.patch("homepage.views.User_service_send_email_authenticated",side_effect=send_email_mock)
    @mock.patch("homepage.views.UserRequest.objects.get", side_effect=User_request_Obj)
    @mock.patch("homepage.views.check_user_authenticated", side_effect=is_authenticated)
    def test_authenticate_user(self, mock_authenticated, mock_request,mock_email):
        service_type_Obj = {
            'service_type': 'Monthly',
            'school': 'Tandon School of Engineering',
            'user':{
                "first_name": "donald",
                "last_name": "trump",
            }

        }
        response = self.client.post("/serviceRequest/", service_type_Obj)
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/homepage/")
        self.assertEqual(response.status_code, 302)

    # def test_view_url_accessible_by_name(self):
    #     response = self.client.get("/homepage/")
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTemplateUsed(response, "homepage.html")

    def test_call_view_success_correct_fields(self):
        requestObj = {
            "service_type": "Weekly",
            "school": "Tandon School of Engineering",
            "department": "Electrical Engineering",
            "cuisine": "[Indian, Pizza]",
        }
        response = self.client.post("/serviceRequest/", requestObj)
        self.assertRedirects(response, "/")

    def test_homepage_department_ajax(self):
        response = self.client.get(
            "homepage/ajax/load_departments/?school_id=Steinhardt%20School%20of%20Culture%2C%20Education%2C%20and%20Human%20Development"
        )
        self.assertTrue(response, '<JsonResponse status_code=200, "application/json">')

    def test_homepage_school_ajax(self):
        response = self.client.get("homepage/ajax/load_school/?department_id=Biology")
        self.assertTrue(response, '<JsonResponse status_code=200, "application/json">')


def all():
    return "all"


class IndexViewTest(TestCase):

    def no_repeat_login(request):
        return True

    @mock.patch("homepage.views.check_index_login", side_effect=no_repeat_login)
    def test_repeat_login(self, mock_index_login):
        response = self.client.get("/homepage/")
        self.assertEqual(response.status_code, 200)


class LogoutViewTest(TestCase):
    def test_logout_without_user_session(self):
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)
