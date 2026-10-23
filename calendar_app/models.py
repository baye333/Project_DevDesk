from django.conf import settings
from django.db import models
from django.urls import reverse


class Event(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events"
    )
    title = models.CharField("Titre", max_length=200)
    description = models.TextField("Description", blank=True)
    start = models.DateTimeField("Début")
    end = models.DateTimeField("Fin")
    all_day = models.BooleanField("Journée entière", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start"]
        verbose_name = "Événement"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("calendar_app:detail", args=[self.pk])
