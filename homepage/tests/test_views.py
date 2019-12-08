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

    def mock_email_string(p1, p2):
        return "abc"

    def mock_email_message(email_subject, message, to):
        class email:
            def __init__(self):
                pass

            def send(p1):
                return "sent"

        return email()

    def mock_user(request):
        class user_for_mock:
            def __init__(self):
                self.first_name = "donald"
                self.email = "abc@nyu,edu"

        return user_for_mock()

    @mock.patch("homepage.views.get_user", side_effect=mock_user)
    @mock.patch("homepage.views.EmailMessage", side_effect=mock_email_message)
    @mock.patch("homepage.views.render_to_string", side_effect=mock_email_string)
    @mock.patch("homepage.views.UserRequest.objects.get", side_effect=User_request_Obj)
    @mock.patch("homepage.views.check_user_authenticated", side_effect=is_authenticated)
    def test_authenticate_user(
        self,
        mock_authenticated,
        mock_request,
        mock_email_string,
        mock_email_message,
        mock_user,
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
        response = self.client.post("/service/", service_type_Obj)
        self.assertEqual(response.status_code, 302)

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

    def mock_email_string(p1, p2):
        return "abc"

    def mock_email_message(email_subject, message, to):
        class email:
            def __init__(self):
                pass

            def send(p1):
                return "sent"

        return email()

    def mock_user(request):
        class user_for_mock:
            def __init__(self):
                self.first_name = "donald"
                self.email = "abc@nyu,edu"

        return user_for_mock()

    @mock.patch("homepage.views.get_user", side_effect=mock_user)
    @mock.patch("homepage.views.EmailMessage", side_effect=mock_email_message)
    @mock.patch("homepage.views.render_to_string", side_effect=mock_email_string)
    @mock.patch("homepage.views.UserRequest", side_effect=UserRequest_mock)
    @mock.patch(
        "homepage.views.UserRequest.objects.get",
        side_effect=User_request_Obj_raise_error(),
    )
    @mock.patch("homepage.views.check_user_authenticated", side_effect=is_authenticated)
    def test_authenticate_user_object_not_exist(
        self,
        mock_authenticated,
        mock_request,
        mock_userrequest,
        mock_email_string,
        mock_email_message,
        mock_user,
    ):
        service_type_Obj = {
            "service_type": "Monthly",
            "school": "Tandon School of Engineering",
            "department": "Computer Science",
            "user": {"first_name": "donald", "last_name": "trump"},
        }
        response = self.client.post("/service/", service_type_Obj)
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/homepage/")
        self.assertEqual(response.status_code, 302)

    def test_homepage_department_ajax(self):
        response = self.client.get(
            "/homepage/ajax/load_departments_homepage/?school_id=College%20of%20Dentistry"
        )
        self.assertTrue(response, '<JsonResponse status_code=200, "application/json">')

    def test_homepage_school_ajax(self):
        response = self.client.get(
            "/homepage/ajax/load_school_homepage/?department_id=Musical%20Theatre"
        )
        self.assertTrue(response, '<JsonResponse status_code=200, "application/json">')

    def test_not_post(self):
        response = self.client.get("/service/")
        self.assertEqual(response.status_code, 200)


class IndexViewTest(TestCase):
    def no_repeat_login(request):
        return True

    @mock.patch("homepage.views.check_login", side_effect=no_repeat_login)
    def test_repeat_login(self, mock_index_login):
        response = self.client.get("/homepage/")
        self.assertEqual(response.status_code, 200)

    def mock_department_filter(school):
        return "filter"

    def User_request_Obj(user):
        class userObj:
            def __init__(self):
                self.school = "school1"
                self.department = "department1"

            def save(self):
                return "Saved"

        return userObj()

    def mock_department(**kargs):
        return ["department1", "department2"]

    def mock_school(**kargs):
        return ["school1", "school2"]

    def no_repeat_login(request):
        return True

    @mock.patch(
        "homepage.views.Department.objects.filter", side_effect=mock_department_filter
    )
    @mock.patch("homepage.views.UserRequest.objects.get", side_effect=User_request_Obj)
    @mock.patch("homepage.views.Department.objects.all", side_effect=mock_department)
    @mock.patch("homepage.views.School.objects.all", side_effect=mock_school)
    @mock.patch("homepage.views.check_login", side_effect=no_repeat_login)
    def test_selected_preference(
        self,
        mock_index_login,
        mock_school,
        mock_department,
        mock_user,
        mock_department_filter,
    ):
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

    def mock_lunchuser(id):
        class lunchuser_for_mock:
            def __init__(self):
                self.username = "Utkarsh"
                self.first_name = "Utkarsh"
                self.last_name = "P"
                self.email = "2345@nyu.edu"
                self.school = "Tandon school"
                self.department = "Computer Science"
                self.Phone = "1233454321"

        return lunchuser_for_mock()

    @mock.patch("homepage.views.UserRequest.objects.get", side_effect=User_request_Obj)
    @mock.patch("homepage.views.LunchNinjaUser.objects.get", side_effect=mock_lunchuser)
    @mock.patch("homepage.views.check_login", side_effect=login_mock)
    def test_correct_setting(self, mock_login, mock_lunchuser, mock_userrequest):
        response = self.client.get("/settings/")
        self.assertEqual(response.status_code, 200)

    def mock_lunchuser(id):
        class lunchuser_for_mock:
            def __init__(self):
                self.username = "Utkarsh"
                self.first_name = "Utkarsh"
                self.last_name = "P"
                self.email = "2345@nyu.edu"
                self.school = "Tandon school"
                self.department = "Computer Science"
                self.Phone = "1234554321"

        return lunchuser_for_mock()

    @mock.patch("homepage.views.UserRequest.objects.get", side_effect=raise_error)
    @mock.patch("homepage.views.LunchNinjaUser.objects.get", side_effect=mock_lunchuser)
    @mock.patch("homepage.views.check_login", side_effect=login_mock)
    def test_incorrect_setting(self, mock_login, mock_lunch, mock_userrequest):
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

    def User_request_Obj_get(**kargs):
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
                self.service_status = True

        return userObj()

    def User_request_Obj_filter(user):
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
                self.service_status = True

            def exists(self):
                return True

        return userObj()

    def mock_request_user(request):
        return "user"

    @mock.patch("homepage.views.get_user", side_effect=mock_request_user)
    @mock.patch(
        "homepage.views.UserRequest.objects.filter", side_effect=User_request_Obj_filter
    )
    @mock.patch(
        "homepage.views.UserRequest.objects.get", side_effect=User_request_Obj_get
    )
    @mock.patch(
        "homepage.views.UserRequestMatch.objects.filter", side_effect=User_match_Obj
    )
    @mock.patch("homepage.views.check_login", side_effect=login_mock)
    def test_match_history_next(
        self,
        mock_login,
        mock_filter,
        mock_request_get,
        mock_request_filter,
        mock_request_user,
    ):
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

    def User_request_Obj_get(**kargs):
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
                self.service_status = True

        return userObj()

    def User_request_Obj_filter(user):
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
                self.service_status = True

            def exists(self):
                return True

        return userObj()

    def mock_request_user(request):
        return "user"

    @mock.patch("homepage.views.get_user", side_effect=mock_request_user)
    @mock.patch(
        "homepage.views.UserRequest.objects.filter", side_effect=User_request_Obj_filter
    )
    @mock.patch(
        "homepage.views.UserRequest.objects.get", side_effect=User_request_Obj_get
    )
    @mock.patch(
        "homepage.views.UserRequestMatch.objects.filter", side_effect=User_match_Obj
    )
    @mock.patch("homepage.views.check_login", side_effect=login_mock)
    def test_match_history_past(
        self,
        mock_login,
        mock_filter,
        mock_request_get,
        mock_request_filter,
        mock_request_user,
    ):
        response = self.client.get("/matchHistory/")
        self.assertEqual(response.status_code, 200)


class FeedbackViewTest(TestCase):
    def mock_feedback(id, match, user, comment):
        class choice_for_mock:
            def __init__(self):
                pass

            def add(p1):
                return "add"

        class feedback_for_mock:
            def __init__(self, id, match, user, comment):
                self.choices = choice_for_mock
                pass

            def save(p1):
                return "saved"

        return feedback_for_mock(id, match, user, comment)

    def mock_question(**kargs):
        class choice_for_mock:
            def __init__(self, label):
                pass

            def get(choice_text):
                return "get"

        class question_for_mock:
            def __init__(self):
                self.choice_set = choice_for_mock

        return question_for_mock()

    def mock_userrequest(id):
        return 1

    def mock_lunchuser(id):
        return 1

    @mock.patch("homepage.views.Question.objects.get", side_effect=mock_question)
    @mock.patch("homepage.views.Feedback", side_effect=mock_feedback)
    @mock.patch(
        "homepage.views.UserRequestMatch.objects.get", side_effect=mock_userrequest
    )
    @mock.patch("homepage.views.LunchNinjaUser.objects.get", side_effect=mock_lunchuser)
    def test_post_feedback(
        self, mock_lunchuser, mock_userreq, feedback_mock, question_mock
    ):
        service_type_Obj = {
            "attendance": "Yes!",
            "experience": 1,
            "restaurant": 1,
            "partner": 1,
            "comment": " hahaha",
        }
        response = self.client.post("/feedback/b'Mi0z'", service_type_Obj)
        self.assertEqual(response.status_code, 302)

    def test_not_matched_feedback_(self):
        response = self.client.get("/feedback/b'Mi0z'")
        self.assertEqual(response.status_code, 200)

    def test_incorrect_get_feedback_link(self):
        response = self.client.get("/feedback/2-3-4")
        self.assertEqual(response.status_code, 200)

    def test_incorrect_get_feedback_link2(self):
        response = self.client.get("/feedback/2-3-4/3232")
        self.assertEqual(response.status_code, 200)

    def mock_match_history_filter(id):
        class match_history_for_mock:
            def __init__(self):
                pass

            def count(id):
                return 2

        return match_history_for_mock()

    def mock_match_history_get(id):
        class match_history_for_mock:
            def __init__(self):
                self.user1 = 100000
                self.user2 = 200000
                pass

            def count(id):
                return 0

        return match_history_for_mock()

    def mock_lunchuser_filter(id):
        class lunch_user_for_mock:
            def __init__(self):
                pass

            def count(id):
                return 0

        return lunch_user_for_mock()

    def mock_lunchuser_get(id):
        class lunch_user_for_mock:
            def __init__(self):
                self.id = 1
                pass

        return lunch_user_for_mock()

    def mock_feedback_filter(self):
        class feedback_for_mock:
            def __init__(self):
                self.id = 1
                pass

            def count(id):
                return 0

    @mock.patch("homepage.views.Feedback", side_effect=mock_feedback_filter)
    @mock.patch(
        "homepage.views.LunchNinjaUser.objects.get", side_effect=mock_lunchuser_get
    )
    @mock.patch(
        "homepage.views.LunchNinjaUser.objects.filter",
        side_effect=mock_lunchuser_filter,
    )
    @mock.patch(
        "homepage.views.UserRequestMatch.objects.get",
        side_effect=mock_match_history_get,
    )
    @mock.patch(
        "homepage.views.UserRequestMatch.objects.filter",
        side_effect=mock_match_history_filter,
    )
    def test_incorrect_get_user_feedback(
        self,
        mock_matchlunchuser_filter,
        mock_matchlunchuser_get,
        mock_lunch_user_filter,
        mock_lunch_user_get,
        mock_feedback_filter,
    ):
        response = self.client.get("/feedback/2-3")
        self.assertEqual(response.status_code, 200)

    def mock_match_history_filter(id):
        class match_history_for_mock:
            def __init__(self):
                pass

            def count(id):
                return 2

        return match_history_for_mock()

    def mock_match_history_get(id):
        class match_history_for_mock:
            def __init__(self):
                self.user1 = 100000
                self.user2 = 200000
                pass

            def count(id):
                return 0

        return match_history_for_mock()

    def mock_lunchuser_filter(id):
        class lunch_user_for_mock:
            def __init__(self):
                pass

            def count(id):
                return 2

        return lunch_user_for_mock()

    def mock_lunchuser_get(id):
        class lunch_user_for_mock:
            def __init__(self):
                self.id = 1
                pass

        return lunch_user_for_mock()

    def mock_feedback_filter(self):
        class feedback_for_mock:
            def __init__(self):
                self.id = 1
                pass

            def count(id):
                return 2

    @mock.patch("homepage.views.Feedback", side_effect=mock_feedback_filter)
    @mock.patch(
        "homepage.views.LunchNinjaUser.objects.get", side_effect=mock_lunchuser_get
    )
    @mock.patch(
        "homepage.views.LunchNinjaUser.objects.filter",
        side_effect=mock_lunchuser_filter,
    )
    @mock.patch(
        "homepage.views.UserRequestMatch.objects.get",
        side_effect=mock_match_history_get,
    )
    @mock.patch(
        "homepage.views.UserRequestMatch.objects.filter",
        side_effect=mock_match_history_filter,
    )
    def test_submitted_feedback(
        self,
        mock_matchlunchuser_filter,
        mock_matchlunchuser_get,
        mock_lunch_user_filter,
        mock_lunch_user_get,
        mock_feedback_filter,
    ):
        response = self.client.get("/feedback/2-3")
        self.assertEqual(response.status_code, 200)

    def mock_match_history_filter(id):
        class match_history_for_mock:
            def __init__(self):
                pass

            def count(id):
                return 2

        return match_history_for_mock()

    def mock_match_history_get(id):
        class match_history_for_mock:
            def __init__(self):
                self.user1 = 1
                self.user2 = 2
                pass

            def count(id):
                return 0

        return match_history_for_mock()

    def mock_lunchuser_filter(id):
        class lunch_user_for_mock:
            def __init__(self):
                pass

            def count(id):
                return 2

        return lunch_user_for_mock()

    def mock_lunchuser_get(id):
        class lunch_user_for_mock:
            def __init__(self):
                self.id = 1
                pass

        return lunch_user_for_mock()

    def mock_feedback_filter(self):
        class feedback_for_mock:
            def __init__(self):
                self.id = 1
                pass

            def count(id):
                return 0

    @mock.patch("homepage.views.Feedback", side_effect=mock_feedback_filter)
    @mock.patch(
        "homepage.views.LunchNinjaUser.objects.get", side_effect=mock_lunchuser_get
    )
    @mock.patch(
        "homepage.views.LunchNinjaUser.objects.filter",
        side_effect=mock_lunchuser_filter,
    )
    @mock.patch(
        "homepage.views.UserRequestMatch.objects.get",
        side_effect=mock_match_history_get,
    )
    @mock.patch(
        "homepage.views.UserRequestMatch.objects.filter",
        side_effect=mock_match_history_filter,
    )
    def test_correct_get_feedback(
        self,
        mock_matchlunchuser_filter,
        mock_matchlunchuser_get,
        mock_lunch_user_filter,
        mock_lunch_user_get,
        mock_feedback_filter,
    ):
        response = self.client.get("/feedback/2-3")
        self.assertEqual(response.status_code, 200)


class AboutViewTest(TestCase):
    def login_mock(request):
        return True

    def get_modeldata(user):
        return {}

    def get_selected_data(self):
        return {}

    @mock.patch("homepage.views.get_selected_data", side_effect=get_selected_data)
    @mock.patch("homepage.views.getModelData", side_effect=get_modeldata)
    @mock.patch("homepage.views.check_login", side_effect=login_mock)
    def test_login_user(self, login_mock, get_modeldata, get_selected_data):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)

    def test_not_login_user(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 302)
