from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("low", "Basse"),
        ("normal", "Normale"),
        ("high", "Haute"),
        ("urgent", "Urgente"),
    )
    STATUS_CHOICES = (
        ("todo", "À faire"),
        ("in_progress", "En cours"),
        ("waiting", "En attente"),
        ("done", "Terminée"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks"
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )
    title = models.CharField("Titre", max_length=200)
    description = models.TextField("Description", blank=True)
    priority = models.CharField("Priorité", max_length=10, choices=PRIORITY_CHOICES, default="normal")
    status = models.CharField("Statut", max_length=20, choices=STATUS_CHOICES, default="todo")
    due_date = models.DateField("Date limite", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["status", "due_date", "-priority"]
        verbose_name = "Tâche"
        verbose_name_plural = "Tâches"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tasks:detail", args=[self.pk])

    @property
    def is_overdue(self):
        if not self.due_date or self.status == "done":
            return False
        return self.due_date < timezone.localdate()
