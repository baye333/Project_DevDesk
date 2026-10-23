from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Project


class ProjectTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user("owner", "o@example.com", "Secret12345")
        self.other = User.objects.create_user("other", "x@example.com", "Secret12345")
        self.project = Project.objects.create(owner=self.owner, title="API", status="active", progress=40)

    def test_owner_crud(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("projects:list"))
        self.assertContains(response, "API")
        response = self.client.post(
            reverse("projects:create"),
            {
                "title": "Site vitrine",
                "description": "HTML",
                "category": "web",
                "technologies": "Django",
                "priority": "high",
                "status": "planning",
                "progress": 10,
                "due_date": "2026-12-01",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(owner=self.owner, title="Site vitrine").exists())
        response = self.client.post(
            reverse("projects:update", args=[self.project.pk]),
            {
                "title": "API v2",
                "description": "",
                "category": "web",
                "technologies": "Django",
                "priority": "normal",
                "status": "active",
                "progress": 55,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "API v2")

    def test_isolation(self):
        self.client.force_login(self.other)
        response = self.client.get(reverse("projects:detail", args=[self.project.pk]))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse("projects:list"))
        self.assertNotContains(response, "API")
