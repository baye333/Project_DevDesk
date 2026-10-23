from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import LearningGoal, Skill


class LearningTests(TestCase):
    def test_create_skill_and_goal(self):
        user = User.objects.create_user("learn", "l@example.com", "Secret12345")
        self.client.force_login(user)
        response = self.client.post(
            reverse("learning:skill_create"),
            {"name": "Python", "category": "langage", "level": "intermediate", "progress": 40},
        )
        self.assertEqual(response.status_code, 302)
        skill = Skill.objects.get(owner=user, name="Python")
        response = self.client.post(
            reverse("learning:goal_create"),
            {
                "title": "Django 5",
                "skill": skill.pk,
                "description": "Maîtriser Django",
                "deadline": timezone.localdate().isoformat(),
                "progress": 10,
                "status": "in_progress",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(LearningGoal.objects.filter(owner=user, title="Django 5").exists())
