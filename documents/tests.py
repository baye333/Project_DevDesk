from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Document


class DocumentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("docs", "docs@example.com", "Secret12345")
        self.other = User.objects.create_user("intrus", "i@example.com", "Secret12345")

    def test_upload_download_and_isolation(self):
        self.client.force_login(self.user)
        upload = SimpleUploadedFile("brief.pdf", b"%PDF-1.4 test", content_type="application/pdf")
        response = self.client.post(
            reverse("documents:create"),
            {"title": "Brief", "category": "specs", "file": upload},
        )
        self.assertEqual(response.status_code, 302)
        document = Document.objects.get(owner=self.user, title="Brief")
        response = self.client.get(reverse("documents:download", args=[document.pk]))
        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.other)
        response = self.client.get(reverse("documents:download", args=[document.pk]))
        self.assertEqual(response.status_code, 404)

    def test_rejects_bad_extension(self):
        self.client.force_login(self.user)
        upload = SimpleUploadedFile("virus.exe", b"MZ", content_type="application/octet-stream")
        response = self.client.post(
            reverse("documents:create"),
            {"title": "Bad", "category": "other", "file": upload},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Document.objects.filter(title="Bad").exists())
