from django.conf import settings
from django.db import models
from django.urls import reverse


class Project(models.Model):
    CATEGORY_CHOICES = (
        ("web", "Web"),
        ("mobile", "Mobile"),
        ("data", "Data"),
        ("devops", "DevOps"),
        ("school", "Scolaire"),
        ("other", "Autre"),
    )
    PRIORITY_CHOICES = (
        ("low", "Basse"),
        ("normal", "Normale"),
        ("high", "Haute"),
        ("urgent", "Urgente"),
    )
    STATUS_CHOICES = (
        ("planning", "Planifié"),
        ("active", "Actif"),
        ("paused", "En pause"),
        ("completed", "Terminé"),
        ("archived", "Archivé"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects"
    )
    title = models.CharField("Titre", max_length=200)
    description = models.TextField("Description", blank=True)
    category = models.CharField("Catégorie", max_length=20, choices=CATEGORY_CHOICES, default="web")
    technologies = models.CharField("Technologies", max_length=255, blank=True)
    priority = models.CharField("Priorité", max_length=10, choices=PRIORITY_CHOICES, default="normal")
    status = models.CharField("Statut", max_length=20, choices=STATUS_CHOICES, default="planning")
    progress = models.PositiveSmallIntegerField("Progression (%)", default=0)
    due_date = models.DateField("Date limite", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:detail", args=[self.pk])

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.progress > 100:
            raise ValidationError({"progress": "La progression doit être comprise entre 0 et 100."})
