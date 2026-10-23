from django.conf import settings
from django.db import models


class Notification(models.Model):
    KIND_CHOICES = (
        ("overdue", "En retard"),
        ("upcoming", "Échéance proche"),
        ("info", "Information"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default="info")
    link = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    fingerprint = models.CharField(max_length=120, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Notification"
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "fingerprint"],
                name="uniq_notification_fingerprint",
                condition=~models.Q(fingerprint=""),
            )
        ]

    def __str__(self):
        return self.title
