from django.conf import settings
from django.db import models
from django.urls import reverse


class Note(models.Model):
    CATEGORY_CHOICES = (
        ("python", "Python"),
        ("django", "Django"),
        ("linux", "Linux"),
        ("docker", "Docker"),
        ("networks", "Réseaux"),
        ("cybersecurity", "Cybersécurité"),
        ("devops", "DevOps"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notes"
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notes",
    )
    title = models.CharField("Titre", max_length=200)
    content = models.TextField("Contenu")
    category = models.CharField("Catégorie", max_length=20, choices=CATEGORY_CHOICES, default="python")
    tags = models.CharField("Tags", max_length=255, blank=True, help_text="Séparés par des virgules")
    is_favorite = models.BooleanField("Favori", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("notes:detail", args=[self.pk])

    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]
