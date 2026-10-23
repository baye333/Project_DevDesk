import uuid
from pathlib import Path

from django.conf import settings
from django.db import models
from django.urls import reverse


def document_upload_to(instance, filename):
    ext = Path(filename).suffix.lower()
    return f"{instance.owner_id}/documents/{uuid.uuid4().hex}{ext}"


class Document(models.Model):
    CATEGORY_CHOICES = (
        ("specs", "Spécifications"),
        ("course", "Cours"),
        ("report", "Rapport"),
        ("invoice", "Facture"),
        ("image", "Image"),
        ("other", "Autre"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="documents"
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documents",
    )
    title = models.CharField("Titre", max_length=200)
    category = models.CharField("Catégorie", max_length=20, choices=CATEGORY_CHOICES, default="other")
    file = models.FileField("Fichier", upload_to=document_upload_to)
    original_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Document"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("documents:detail", args=[self.pk])

    @property
    def extension(self):
        return Path(self.file.name).suffix.lower().lstrip(".")
