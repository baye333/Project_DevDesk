from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Note


class NoteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("noteuser", "n@example.com", "Secret12345")
        self.other = User.objects.create_user("other", "o@example.com", "Secret12345")
        self.note = Note.objects.create(
            owner=self.user,
            title="ORM Django",
            content="Note.objects.filter(owner=user)",
            category="django",
            tags="orm,queryset",
        )

    def test_search_and_detail(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("notes:list"), {"q": "ORM"})
        self.assertContains(response, "ORM Django")
        response = self.client.get(reverse("notes:detail", args=[self.note.pk]))
        self.assertContains(response, "queryset")

    def test_isolation(self):
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(reverse("notes:detail", args=[self.note.pk])).status_code, 404)
