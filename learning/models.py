from django.conf import settings
from django.db import models
from django.urls import reverse


class Skill(models.Model):
    LEVEL_CHOICES = (
        ("beginner", "Débutant"),
        ("intermediate", "Intermédiaire"),
        ("advanced", "Avancé"),
        ("expert", "Expert"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="skills"
    )
    name = models.CharField("Compétence", max_length=150)
    category = models.CharField("Catégorie", max_length=80, blank=True)
    level = models.CharField("Niveau", max_length=20, choices=LEVEL_CHOICES, default="beginner")
    progress = models.PositiveSmallIntegerField("Progression (%)", default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Compétence"

    def __str__(self):
        return self.name


class LearningGoal(models.Model):
    STATUS_CHOICES = (
        ("not_started", "Non commencé"),
        ("in_progress", "En cours"),
        ("completed", "Terminé"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="learning_goals"
    )
    skill = models.ForeignKey(
        Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name="goals"
    )
    title = models.CharField("Objectif / formation", max_length=200)
    description = models.TextField("Description", blank=True)
    deadline = models.DateField("Échéance", null=True, blank=True)
    progress = models.PositiveSmallIntegerField("Progression (%)", default=0)
    status = models.CharField("Statut", max_length=20, choices=STATUS_CHOICES, default="not_started")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Objectif d'apprentissage"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("learning:goal_detail", args=[self.pk])


class LearningSession(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="learning_sessions"
    )
    goal = models.ForeignKey(
        LearningGoal, on_delete=models.SET_NULL, null=True, blank=True, related_name="sessions"
    )
    skill = models.ForeignKey(
        Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name="sessions"
    )
    title = models.CharField("Session", max_length=200)
    duration_minutes = models.PositiveIntegerField("Durée (minutes)", default=30)
    notes = models.TextField("Notes", blank=True)
    date = models.DateField("Date")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name = "Session d'apprentissage"

    def __str__(self):
        return self.title


class LearningResource(models.Model):
    TYPE_CHOICES = (
        ("article", "Article"),
        ("video", "Vidéo"),
        ("course", "Cours"),
        ("docs", "Documentation"),
        ("other", "Autre"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="learning_resources"
    )
    goal = models.ForeignKey(
        LearningGoal, on_delete=models.SET_NULL, null=True, blank=True, related_name="resources"
    )
    skill = models.ForeignKey(
        Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name="resources"
    )
    title = models.CharField("Titre", max_length=200)
    url = models.URLField("Lien")
    resource_type = models.CharField("Type", max_length=20, choices=TYPE_CHOICES, default="article")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Ressource"

    def __str__(self):
        return self.title
