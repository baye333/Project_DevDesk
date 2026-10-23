from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthTests(TestCase):
    def test_register_login_logout(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "baye",
                "email": "baye@example.com",
                "password1": "DevDeskPass123",
                "password2": "DevDeskPass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="baye").exists())
        self.client.logout()
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "baye", "password": "DevDeskPass123"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard:home"))
        response = self.client.post(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 302)

    def test_private_pages_require_login(self):
        response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_profile_page(self):
        user = User.objects.create_user("ada", "ada@example.com", "Secret12345")
        self.client.force_login(user)
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("accounts:profile_edit"),
            {
                "display_name": "Ada",
                "bio": "Dev",
                "job_title": "Ingénieure",
                "website": "",
                "theme": "light",
                "first_name": "Ada",
                "last_name": "Lovelace",
                "email": "ada@example.com",
            },
        )
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.first_name, "Ada")
        self.assertEqual(user.profile.theme, "light")
