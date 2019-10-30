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


class LogoutViewTest(TestCase):
    def test_logout_without_user_session(self):
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)
