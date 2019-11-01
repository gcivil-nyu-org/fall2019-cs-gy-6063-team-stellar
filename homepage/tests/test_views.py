from django.test import TestCase


class UserserviceViewTest(TestCase):
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


class LogoutViewTest(TestCase):
    def test_logout_without_user_session(self):
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)
