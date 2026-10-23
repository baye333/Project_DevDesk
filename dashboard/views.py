from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from documents.models import Document
from learning.models import LearningGoal, LearningSession
from notes.models import Note
from projects.models import Project
from tasks.models import Task


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        today = timezone.localdate()
        soon = today + timedelta(days=7)

        projects = Project.objects.filter(owner=user)
        tasks = Task.objects.filter(owner=user)
        notes = Note.objects.filter(owner=user)

        task_counts = tasks.aggregate(
            todo=Count("id", filter=Q(status="todo")),
            in_progress=Count("id", filter=Q(status="in_progress")),
            waiting=Count("id", filter=Q(status="waiting")),
            done=Count("id", filter=Q(status="done")),
            urgent=Count("id", filter=Q(priority="urgent") & ~Q(status="done")),
            overdue=Count("id", filter=Q(due_date__lt=today) & ~Q(status="done")),
        )
        project_status = list(
            projects.values("status").annotate(total=Count("id")).order_by("status")
        )
        upcoming_tasks = tasks.exclude(status="done").filter(
            due_date__isnull=False, due_date__gte=today, due_date__lte=soon
        ).order_by("due_date")[:8]
        overdue_tasks = tasks.exclude(status="done").filter(due_date__lt=today).order_by("due_date")[:8]
        recent_notes = notes[:6]
        active_projects = projects.exclude(status__in=["archived"]).order_by("-updated_at")[:6]
        upcoming_projects = projects.exclude(status__in=["completed", "archived"]).filter(
            due_date__isnull=False, due_date__gte=today
        ).order_by("due_date")[:6]
        sessions = LearningSession.objects.filter(owner=user)[:5]
        goals = LearningGoal.objects.filter(owner=user).exclude(status="completed")[:5]
        docs_count = Document.objects.filter(owner=user).count()

        context = {
            "project_count": projects.count(),
            "task_counts": task_counts,
            "docs_count": docs_count,
            "notes_count": notes.count(),
            "project_status": project_status,
            "upcoming_tasks": upcoming_tasks,
            "overdue_tasks": overdue_tasks,
            "recent_notes": recent_notes,
            "active_projects": active_projects,
            "upcoming_projects": upcoming_projects,
            "sessions": sessions,
            "goals": goals,
            "chart_tasks": [
                task_counts["todo"] or 0,
                task_counts["in_progress"] or 0,
                task_counts["waiting"] or 0,
                task_counts["done"] or 0,
            ],
        }
        return render(request, "dashboard/home.html", context)


class SearchView(LoginRequiredMixin, View):
    def get(self, request):
        q = request.GET.get("q", "").strip()
        results = {"projects": [], "tasks": [], "notes": [], "documents": []}
        if q:
            results["projects"] = Project.objects.filter(owner=request.user).filter(
                Q(title__icontains=q) | Q(description__icontains=q) | Q(technologies__icontains=q)
            )[:15]
            results["tasks"] = Task.objects.filter(owner=request.user).filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )[:15]
            results["notes"] = Note.objects.filter(owner=request.user).filter(
                Q(title__icontains=q) | Q(content__icontains=q) | Q(tags__icontains=q)
            )[:15]
            results["documents"] = Document.objects.filter(owner=request.user).filter(
                Q(title__icontains=q) | Q(original_name__icontains=q)
            )[:15]
        return render(request, "dashboard/search.html", {"q": q, "results": results})
