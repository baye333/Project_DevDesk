from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from projects.models import Project
from tasks.models import Task

from .models import Notification


def sync_deadline_notifications(user):
    today = timezone.localdate()
    soon = today + timedelta(days=3)

    overdue_tasks = Task.objects.filter(owner=user).exclude(status="done").filter(due_date__lt=today)
    for task in overdue_tasks:
        fingerprint = f"overdue-task-{task.pk}-{task.due_date}"
        Notification.objects.get_or_create(
            owner=user,
            fingerprint=fingerprint,
            defaults={
                "title": "Tâche en retard",
                "message": f"« {task.title} » était due le {task.due_date:%d/%m/%Y}.",
                "kind": "overdue",
                "link": reverse("tasks:detail", args=[task.pk]),
            },
        )

    upcoming_tasks = (
        Task.objects.filter(owner=user)
        .exclude(status="done")
        .filter(due_date__gte=today, due_date__lte=soon)
    )
    for task in upcoming_tasks:
        fingerprint = f"upcoming-task-{task.pk}-{task.due_date}"
        Notification.objects.get_or_create(
            owner=user,
            fingerprint=fingerprint,
            defaults={
                "title": "Échéance proche",
                "message": f"« {task.title} » arrive à échéance le {task.due_date:%d/%m/%Y}.",
                "kind": "upcoming",
                "link": reverse("tasks:detail", args=[task.pk]),
            },
        )

    upcoming_projects = Project.objects.filter(
        owner=user, due_date__gte=today, due_date__lte=soon
    ).exclude(status__in=["completed", "archived"])
    for project in upcoming_projects:
        fingerprint = f"upcoming-project-{project.pk}-{project.due_date}"
        Notification.objects.get_or_create(
            owner=user,
            fingerprint=fingerprint,
            defaults={
                "title": "Projet bientôt dû",
                "message": f"« {project.title} » arrive à échéance le {project.due_date:%d/%m/%Y}.",
                "kind": "upcoming",
                "link": reverse("projects:detail", args=[project.pk]),
            },
        )
