from django.test import TestCase
from unittest import mock
from ..models import UserRequest
from datetime import datetime, timezone, timedelta
from django.core.exceptions import ObjectDoesNotExist


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

        class interest_for_mock:
            def __init__(self):
                pass

            def add(**kargs):
                return "Added"

            def clear(**kargs):
                return "Cleared"

        class days_for_mock:
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
                self.interests = interest_for_mock
                self.days = days_for_mock

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

    def send_email_mock(self, p2, p3, p4, p5, p6, p7):
        pass

    @mock.patch(
        "homepage.views.User_service_send_email_authenticated",
        side_effect=send_email_mock,
    )
    @mock.patch("homepage.views.UserRequest.objects.get", side_effect=User_request_Obj)
    @mock.patch("homepage.views.Days_left.objects.get", side_effect=Days_Obj)
    @mock.patch("homepage.views.check_user_authenticated", side_effect=is_authenticated)
    def test_authenticate_user(
        self, mock_authenticated, mock_dayleft, mock_request, mock_email
    ):
        service_type_Obj = {
            "service_type": "Monthly",
            "school": "Tandon School of Engineering",
            "department": "Computer Science",
            "user": {
                "first_name": "donald",
                "last_name": "trump",
                "mail": "2345@nyu.edu",
            },
        }
        response = self.client.post("/serviceRequest/", service_type_Obj)
        self.assertEqual(response.status_code, 302)

    # def is_authenticated(self):
    #     return False
    #
    # @mock.patch("homepage.views.check_user_authenticated", side_effect=is_authenticated)
    # def test_not_authenticate_user(
    #     self, mock_authenticated
    # ):
    #     service_type_Obj = {
    #         "service_type": "Monthly",
    #         "school": "Tandon School of Engineering",
    #         "department": "Computer Science",
    #         "user": {"first_name": "donald", "last_name": "trump","mail":"2345@nyu.edu"},
    #     }
    #     response = self.client.post("/serviceRequest/", service_type_Obj)
    #     self.assertEqual(response.status_code, 302)

    def User_request_Obj_raise_error(**kargs):
        class cuisine_for_mock:
            def __init__(self):
                pass

            def clear(**kargs):
                raise ObjectDoesNotExist

            def add(**kargs):
                return "Added"

        class userObj:
            def __init__(self):
                self.service_type = "Monthly"
                self.school = "Tandon School of Engineering"
                self.cuisines = cuisine_for_mock

            def save(self):
                return "saved"

        return userObj()

    def UserRequest_mock(**kargs):
        class cuisine_for_mock:
            def __init__(self):
                pass

            def clear(**kargs):
                return "Cleared"

            def add(**kargs):
                return "Added"

        class interest_for_mock:
            def __init__(self):
                pass

            def add(**kargs):
                return "Added"

            def clear(**kargs):
                return "Cleared"

        class days_for_mock:
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
                self.interests = interest_for_mock
                self.days = days_for_mock

            def save(self):
                return "Saved"

        return userObj()

    @mock.patch("homepage.views.UserRequest", side_effect=UserRequest_mock)
    @mock.patch(
        "homepage.views.User_service_send_email_authenticated",
        side_effect=send_email_mock,
    )
    @mock.patch(
        "homepage.views.UserRequest.objects.get",
        side_effect=User_request_Obj_raise_error(),
    )
    @mock.patch("homepage.views.check_user_authenticated", side_effect=is_authenticated)
    def test_authenticate_user_object_not_exist(
        self, mock_authenticated, mock_request, mock_email, mock_userrequest
    ):
        service_type_Obj = {
            "service_type": "Monthly",
            "school": "Tandon School of Engineering",
            "department": "Computer Science",
            "user": {"first_name": "donald", "last_name": "trump"},
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

    # @mock.patch("homepage.views.UserRequest.objects.get", side_effect=User_request_Obj_raise_error())
    # @mock.patch("homepage.views.check_user_authenticated", side_effect=is_authenticated)
    # def test_call_view_success_correct_fields(self):
    #     requestObj = {
    #         "service_type": "Weekly",
    #         "school": "Tandon School of Engineering",
    #         "department": "Electrical Engineering",
    #         "cuisine": "[Indian, Pizza]",
    #     }
    #     response = self.client.post("/serviceRequest/", requestObj)
    #     self.assertRedirects(response, "/")

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


class ToggleViewTest(TestCase):
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

        class interest_for_mock:
            def __init__(self):
                pass

            def add(**kargs):
                return "Added"

            def clear(**kargs):
                return "Cleared"

        class userObj:
            def __init__(self):
                self.service_type = "Monthly"
                self.school = "Tandon School of Engineering"
                self.cuisines = cuisine_for_mock
                self.interests = interest_for_mock
                self.service_status = True

            def save(self):
                return "Saved"

        return userObj()

    @mock.patch("homepage.views.UserRequest.objects.get", side_effect=User_request_Obj)
    @mock.patch("homepage.views.check_user_authenticated", side_effect=is_authenticated)
    def test_authenticate_user(self, mock_authenticated, mock_request):
        service_type_Obj = {
            "service_type": "Monthly",
            "school": "Tandon School of Engineering",
            "department": "Computer Science",
            "user": {"first_name": "donald", "last_name": "trump"},
            "service_status": "true",
        }
        response = self.client.post("/toggle-service/", service_type_Obj)
        self.assertEqual(response.status_code, 200)

    def test_not_authenticate_user(self):
        service_type_Obj = {
            "service_type": "Monthly",
            "school": "Tandon School of Engineering",
            "department": "Computer Science",
            "user": {"first_name": "donald", "last_name": "trump"},
            "service_status": "true",
        }
        response = self.client.post("/toggle-service/", service_type_Obj)
        self.assertEqual(response.status_code, 302)


class SettingViewTest(TestCase):
    def User_request_Obj(**kargs):
        class cuisine_for_mock:
            def __init__(self, name):
                self.name = name
                pass

        class day_for_mock:
            def __init__(self, day):
                self.day = day

            def clear(**kargs):
                return "Cleared"

            def add(**kargs):
                return "Added"

            def save(**kargs):
                return "save"

            def weekday(**kargs):
                return 1

        class days_for_mock:
            def all(**kargs):
                return [
                    day_for_mock("Friday"),
                    day_for_mock("Friday"),
                    day_for_mock("Friday"),
                ]

        class interest_for_mock:
            def __init__(self, name):
                self.name = name

            def add(**kargs):
                return "Added"

            def clear(**kargs):
                return "Cleared"

        class cuisines_for_mock:
            def __init__(self, name):
                pass

            def all(**kargs):
                return [
                    cuisine_for_mock("American"),
                    cuisine_for_mock("Indian"),
                    cuisine_for_mock("Chinese"),
                ]

        class interests_for_mock:
            def __init__(self, name):
                pass

            def all(**kargs):
                return [
                    interest_for_mock("parties"),
                    interest_for_mock("networking"),
                    interest_for_mock("homework"),
                ]

        class userObj:
            def __init__(self):
                self.service_type = "Monthly"
                self.school = "Tandon School of Engineering"
                self.time_stamp = "2019-11-6"
                self.department = "Computer Science"
                self.service_status = True
                self.cuisines = cuisines_for_mock
                self.interests = interests_for_mock
                self.department_priority = 9
                self.cuisines_priority = 4
                self.interests_priority = 8
                self.days = days_for_mock
                self.available_date = day_for_mock

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

        class restaurant_for_mock:
            def __init__(self, name):
                self.name = name
                pass

        class restaurants_for_mock:
            def __init__(self):
                pass

            def all(**kargs):
                return [
                    restaurant_for_mock("McDonald's"),
                    restaurant_for_mock("KFC"),
                    restaurant_for_mock("Burger king"),
                ]

        class match_userObj:
            def __init__(self):

                self.user2 = username()
                self.user1 = username()
                self.match_time = datetime.now(timezone.utc) + timedelta(days=1)
                self.restaurants = restaurants_for_mock

        class result:
            def __init__(self):
                pass

            def order_by(self, p):
                return [match_userObj(), match_userObj()]

        return result()

    def User_request_Obj(**kargs):
        class interest_for_mock:
            def __init__(self, name):
                self.name = name

            def add(**kargs):
                return "Added"

            def clear(**kargs):
                return "Cleared"

        class interests_for_mock:
            def __init__(self, name):
                pass

            def all(**kargs):
                return [
                    interest_for_mock("parties"),
                    interest_for_mock("networking"),
                    interest_for_mock("homework"),
                ]

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
                self.interests = interests_for_mock

        return userObj()

    @mock.patch("homepage.views.UserRequest.objects.get", side_effect=User_request_Obj)
    @mock.patch(
        "homepage.views.UserRequestMatch.objects.filter", side_effect=User_match_Obj
    )
    @mock.patch("homepage.views.check_login", side_effect=login_mock)
    def test_match_history_next(self, mock_login, mock_filter, mock_request):
        response = self.client.get("/matchHistory/")
        self.assertEqual(response.status_code, 200)

    def test_not_login(self):
        response = self.client.get("/matchHistory/")
        self.assertEqual(response.status_code, 302)

    def User_match_Obj(a):
        class username:
            def __init__(self):
                self.first_name = "donald"
                self.last_name = "trump"
                self.email = "1234@nyu.edu"
                self.school = "Tandon School of Engineering"
                self.department = "Electrical Engineering"

        class restaurant_for_mock:
            def __init__(self, name):
                self.name = name
                pass

        class restaurants_for_mock:
            def __init__(self):
                pass

            def all(**kargs):
                return [
                    restaurant_for_mock("McDonald's"),
                    restaurant_for_mock("KFC"),
                    restaurant_for_mock("Burger king"),
                ]

        class match_userObj:
            def __init__(self):

                self.user2 = username()
                self.user1 = username()
                self.match_time = datetime.now(timezone.utc) - timedelta(days=1)
                self.restaurants = restaurants_for_mock

        class result:
            def __init__(self):
                pass

            def order_by(self, p):
                return [match_userObj(), match_userObj()]

        return result()

    def User_request_Obj(**kargs):
        class interest_for_mock:
            def __init__(self, name):
                self.name = name

            def add(**kargs):
                return "Added"

            def clear(**kargs):
                return "Cleared"

        class interests_for_mock:
            def __init__(self, name):
                pass

            def all(**kargs):
                return [
                    interest_for_mock("parties"),
                    interest_for_mock("networking"),
                    interest_for_mock("homework"),
                ]

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
                self.interests = interests_for_mock

        return userObj()

    @mock.patch("homepage.views.UserRequest.objects.get", side_effect=User_request_Obj)
    @mock.patch(
        "homepage.views.UserRequestMatch.objects.filter", side_effect=User_match_Obj
    )
    @mock.patch("homepage.views.check_login", side_effect=login_mock)
    def test_match_history_past(self, mock_login, mock_filter, mock_request):
        response = self.client.get("/matchHistory/")
        self.assertEqual(response.status_code, 200)


class FeedbackViewTest(TestCase):
    def test_post_feedback(self):
        service_type_Obj = {
            "attendance": "Yes!",
            "experience": 1,
            "restaurant": 1,
            "partner": 1,
            "comment": " hahaha",
        }
        response = self.client.post("/feedback/2-3", service_type_Obj)
        self.assertEqual(response.status_code, 302)

    def test_get_feedback(self):

        response = self.client.get("/feedback/2-3")
        self.assertEqual(response.status_code, 200)
