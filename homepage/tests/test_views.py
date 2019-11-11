from django.test import TestCase
from unittest import mock
from ..models import UserRequest


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
                self.service_type = "Monthly"
                self.school = "Tandon School of Engineering"
                self.cuisines = cuisine_for_mock

            def save(self):
                return "Saved"

        return userObj()

    def Days_Obj(**kargs):
        class days_for_mock:
            def __init__(self):
                pass

            def clear(**kargs):
                return "Cleared"

            def add(**kargs):
                return "Added"

            def save(**kargs):
                return "save"

        class userObj:
            def __init__(self):
                self.service_type = "Monthly"
                self.school = "Tandon School of Engineering"

            def save(self):
                return "Saved"

        return days_for_mock

    def send_email_mock(self, p2, p3):
        pass

    @mock.patch(
        "homepage.views.User_service_send_email_authenticated",
        side_effect=send_email_mock,
    )
    @mock.patch("homepage.views.UserRequest.objects.get", side_effect=User_request_Obj)
    @mock.patch("homepage.views.Days_left.objects.get", side_effect=Days_Obj)
    @mock.patch("homepage.views.check_user_authenticated", side_effect=is_authenticated)
    def test_authenticate_user(self, mock_authenticated, mock_dayleft, mock_request, mock_email):
        service_type_Obj = {
            "service_type": "Monthly",
            "school": "Tandon School of Engineering",
            "department": "Computer Science",
            "user": {"first_name": "donald", "last_name": "trump"},
        }
        response = self.client.post("/serviceRequest/", service_type_Obj)
        self.assertEqual(response.status_code, 302)

    # def User_request_Obj_raise_error(**kargs):
    #     class cuisine_for_mock:
    #         def __init__(self):
    #             pass
    #
    #         def clear(**kargs):
    #             raise  ObjectDoesNotExist
    #
    #         def add(**kargs):
    #             return "Added"
    #
    #     class userObj:
    #         def __init__(self):
    #             self.service_type = "Monthly"
    #             self.school = "Tandon School of Engineering"
    #             self.cuisines = cuisine_for_mock
    #
    #         def save(self):
    #             return  "saved"
    #
    #     return userObj()
    # @mock.patch(
    #     "homepage.views.User_service_send_email_authenticated",
    #     side_effect=send_email_mock,
    # )
    # @mock.patch("homepage.views.UserRequest.objects.get", side_effect=User_request_Obj_raise_error())
    # @mock.patch("homepage.views.check_user_authenticated", side_effect=is_authenticated)
    # def test_authenticate_user_object_not_exist(self, mock_authenticated, mock_request, mock_email):
    #     service_type_Obj = {
    #         "service_type": "Monthly",
    #         "school": "Tandon School of Engineering",
    #         "department": "Computer Science",
    #         "user": {"first_name": "donald", "last_name": "trump"},
    #     }
    #     response = self.client.post("/serviceRequest/", service_type_Obj)
    #     self.assertEqual(response.status_code, 302)

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

    def request_start(request):
        return True

    @mock.patch("homepage.views.check_ajax_department", side_effect=request_start)
    def test_homepage_department_ajax(self, mock_head_chek):
        response = self.client.get(
            "/homepage/ajax/load_departments_homepage/?school_id=College%20of%20Dentistry"
        )
        self.assertTrue(response, '<JsonResponse status_code=200, "application/json">')

    @mock.patch("homepage.views.check_ajax_school", side_effect=request_start)
    def test_homepage_school_ajax(self, mock_head_chek):
        response = self.client.get(
            "/homepage/ajax/load_school_homepage/?department_id=Musical%20Theatre"
        )
        self.assertTrue(response, '<JsonResponse status_code=200, "application/json">')

    def test_not_post(self):
        response = self.client.get("/serviceRequest/")
        self.assertEqual(response.status_code, 302)


class IndexViewTest(TestCase):
    def no_repeat_login(request):
        return True

    @mock.patch("homepage.views.check_login", side_effect=no_repeat_login)
    def test_repeat_login(self, mock_index_login):
        response = self.client.get("/homepage/")
        self.assertEqual(response.status_code, 200)


class LogoutViewTest(TestCase):
    def test_logout_without_user_session(self):
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)


class SettingViewTest(TestCase):
    def User_request_Obj(**kargs):
        class cuisine_for_mock:
            def __init__(self, name):
                self.name = name
                pass

        class cuisines_for_mock:
            def __init__(self, name):
                pass

            def all(**kargs):
                return [
                    cuisine_for_mock("American"),
                    cuisine_for_mock("Indian"),
                    cuisine_for_mock("Chinese"),
                ]

        class userObj:
            def __init__(self):
                self.service_type = "Monthly"
                self.school = "Tandon School of Engineering"
                self.time_stamp = "2019-11-6"
                self.department = "Computer Science"
                self.service_status = True
                self.cuisines = cuisines_for_mock

        return userObj()

    def raise_error(**kargs):

        raise UserRequest.DoesNotExist

    def login_mock(request):

        return True

    @mock.patch("homepage.views.UserRequest.objects.get", side_effect=User_request_Obj)
    @mock.patch("homepage.views.check_login", side_effect=login_mock)
    def test_correct_setting(self, mock_login, mock_userrequest):
        response = self.client.get("/settings/")
        self.assertEqual(response.status_code, 200)

    @mock.patch("homepage.views.UserRequest.objects.get", side_effect=raise_error)
    @mock.patch("homepage.views.check_login", side_effect=login_mock)
    def test_incorrect_setting(self, mock_login, mock_userrequest):
        response = self.client.get("/settings/")
        self.assertEqual(response.status_code, 200)

    def test_not_login(self):
        response = self.client.get("/settings/")
        self.assertEqual(response.status_code, 302)


class MatchHistoryTest(TestCase):
    def login_mock(request):
        return True

    def User_match_Obj(a):
        class username:
            def __init__(self):
                self.first_name = "donald"
                self.last_name = "trump"
                self.email = "1234@nyu.edu"
                self.school = "Tandon School of Engineering"
                self.department = "Electrical Engineering"

        class match_userObj:
            def __init__(self):

                self.user2 = username()
                self.user1 = username()
                self.match_time = "2019-11-5"

        class result:
            def __init__(self):
                pass

            def order_by(self, p):
                return [match_userObj(), match_userObj()]

        return result()

    def User_request_Obj(**kargs):
        class cuisine_for_mock:
            def __init__(self, name):
                self.name = name
                pass

        class cuisines_for_mock:
            def __init__(self, name):
                pass

            def all(**kargs):
                return [
                    cuisine_for_mock("American"),
                    cuisine_for_mock("Indian"),
                    cuisine_for_mock("Chinese"),
                ]

        class userObj:
            def __init__(self):
                self.service_type = "Monthly"
                self.school = "Tandon School of Engineering"
                self.time_stamp = "2019-11-6"
                self.department = "Computer Science"
                self.service_status = True
                self.cuisines = cuisines_for_mock

        return userObj()

    @mock.patch("homepage.views.UserRequest.objects.get", side_effect=User_request_Obj)
    @mock.patch(
        "homepage.views.UserRequestMatch.objects.filter", side_effect=User_match_Obj
    )
    @mock.patch("homepage.views.check_login", side_effect=login_mock)
    def test_match_history(self, mock_login, mock_filter, mock_request):
        response = self.client.get("/matchHistory/")
        self.assertEqual(response.status_code, 200)

    def test_not_login(self):
        response = self.client.get("/matchHistory/")
        self.assertEqual(response.status_code, 302)
