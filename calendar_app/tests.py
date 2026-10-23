from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Event


class CalendarTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("cal", "c@example.com", "Secret12345")
        self.other = User.objects.create_user("nope", "n@example.com", "Secret12345")
        now = timezone.now()
        self.event = Event.objects.create(
            owner=self.user,
            title="Revue de code",
            start=now,
            end=now + timedelta(hours=1),
        )

    def test_month_view_and_isolation(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("calendar_app:month"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Revue de code")
        self.client.force_login(self.other)
        response = self.client.get(reverse("calendar_app:detail", args=[self.event.pk]))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse("calendar_app:week"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Revue de code")
