from django.test import TestCase
from homepage.models import School, Department, Restaurant, Cuisine, UserRequest


class SchoolModelTest(TestCase):
    def test_string_representation(self):
        entry = School(name="Tandon School of Engineering")
        self.assertEqual(str(entry), entry.name)


class DepartmentModelTest(TestCase):
    def test_string_representation(self):
        entry = Department(name="Computer Science", school=1)
        self.assertEqual(str(entry), entry.name)


class RestaurantModelTest(TestCase):
    def test_string_representation(self):
        entry = Restaurant(
            name="KIMCHEE KOREAN RESTAURANT",
            cuisine="Korean",
            score="13",
            borough="Brooklyn",
            building="9324",
            street="3 AVENUE",
            zipcode="11209",
            phone="7185675741",
            latitude="40.618412610578",
            longitude="-74.033131508195",
        )
        self.assertEqual(str(entry), entry.name)


class CuisineModelTest(TestCase):
    def test_string_representation(self):
        entry = Cuisine(name="Chinese")
        self.assertEqual(str(entry), entry.name)


class UserRequestModelTest(TestCase):
    def test_string_representation(self):
        entry = UserRequest(
            user_id=23,
            service_type="Monthly",
            time_stamp="2019-11-1",
            school="Tandon School of Engineering",
            department="Computer Engineering",
        )
        self.assertEqual(str(entry), entry.service_type)
