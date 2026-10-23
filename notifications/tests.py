from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from tasks.models import Task

from .models import Notification
from .services import sync_deadline_notifications


class NotificationTests(TestCase):
    def test_overdue_sync(self):
        user = User.objects.create_user("nuser", "n@example.com", "Secret12345")
        Task.objects.create(
            owner=user,
            title="Deadline ratée",
            due_date=timezone.localdate() - timedelta(days=1),
            status="todo",
        )
        sync_deadline_notifications(user)
        self.assertTrue(Notification.objects.filter(owner=user, kind="overdue").exists())
        self.client.force_login(user)
        response = self.client.get(reverse("notifications:list"))
        self.assertContains(response, "Deadline ratée")
