from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def avatar_upload_to(instance, filename):
    ext = filename.rsplit(".", 1)[-1].lower()
    return f"{instance.user_id}/avatars/avatar.{ext}"


class Profile(models.Model):
    THEME_CHOICES = (
        ("dark", "Sombre"),
        ("light", "Clair"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    display_name = models.CharField("Nom affiché", max_length=120, blank=True)
    bio = models.TextField("Bio", blank=True)
    job_title = models.CharField("Poste / formation", max_length=120, blank=True)
    website = models.URLField("Site web", blank=True)
    avatar = models.ImageField("Avatar", upload_to=avatar_upload_to, blank=True)
    theme = models.CharField(
        "Thème", max_length=10, choices=THEME_CHOICES, default="dark"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"

    def __str__(self):
        return self.display_name or self.user.get_username()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, display_name=instance.get_username())
    else:
        Profile.objects.get_or_create(user=instance, defaults={"display_name": instance.get_username()})
