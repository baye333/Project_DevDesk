from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from notes.models import Note
from projects.models import Project
from tasks.models import Task


class DashboardTests(TestCase):
    def test_stats_use_real_data(self):
        user = User.objects.create_user("dash", "d@example.com", "Secret12345")
        other = User.objects.create_user("ghost", "g@example.com", "Secret12345")
        Project.objects.create(owner=user, title="Mine", progress=20)
        Project.objects.create(owner=other, title="Theirs", progress=90)
        Task.objects.create(owner=user, title="A", status="todo")
        Task.objects.create(owner=user, title="B", status="done")
        Task.objects.create(
            owner=user,
            title="Late",
            status="todo",
            due_date=timezone.localdate() - timedelta(days=2),
        )
        Note.objects.create(owner=user, title="Memo", content="hello", category="python")
        self.client.force_login(user)
        response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["project_count"], 1)
        self.assertEqual(response.context["task_counts"]["todo"], 2)
        self.assertEqual(response.context["task_counts"]["done"], 1)
        self.assertEqual(response.context["task_counts"]["overdue"], 1)
        self.assertContains(response, "Memo")
        self.assertNotContains(response, "Theirs")

    def test_search(self):
        user = User.objects.create_user("seek", "s@example.com", "Secret12345")
        Project.objects.create(owner=user, title="DevDesk core")
        self.client.force_login(user)
        response = self.client.get(reverse("dashboard:search"), {"q": "DevDesk"})
        self.assertContains(response, "DevDesk core")
