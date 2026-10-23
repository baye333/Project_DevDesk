from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Task


class TaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("dev", "d@example.com", "Secret12345")
        self.other = User.objects.create_user("spy", "s@example.com", "Secret12345")
        self.task = Task.objects.create(
            owner=self.user,
            title="Écrire les tests",
            status="todo",
            priority="urgent",
            due_date=timezone.localdate() - timedelta(days=1),
        )

    def test_list_and_overdue(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:list"))
        self.assertContains(response, "Écrire les tests")
        self.assertContains(response, "retard")

    def test_kanban_and_status(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("tasks:kanban"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("tasks:status", args=[self.task.pk]), {"status": "done"})
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "done")

    def test_isolation(self):
        self.client.force_login(self.other)
        response = self.client.get(reverse("tasks:detail", args=[self.task.pk]))
        self.assertEqual(response.status_code, 404)
        response = self.client.post(reverse("tasks:status", args=[self.task.pk]), {"status": "done"})
        self.assertEqual(response.status_code, 404)
