from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View

from accounts.mixins import AssignOwnerMixin, OwnerQuerySetMixin
from .forms import TaskFilterForm, TaskForm
from .models import Task


class TaskListView(OwnerQuerySetMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related("project")
        form = TaskFilterForm(self.request.GET, user=self.request.user)
        if form.is_valid():
            data = form.cleaned_data
            if data.get("q"):
                qs = qs.filter(title__icontains=data["q"])
            if data.get("status"):
                qs = qs.filter(status=data["status"])
            if data.get("priority"):
                qs = qs.filter(priority=data["priority"])
            if data.get("project"):
                qs = qs.filter(project=data["project"])
            sort = data.get("sort") or "-updated_at"
            allowed = {"-updated_at", "due_date", "priority", "title"}
            if sort in allowed:
                qs = qs.order_by(sort)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = TaskFilterForm(self.request.GET, user=self.request.user)
        return context


class TaskKanbanView(OwnerQuerySetMixin, TemplateView):
    template_name = "tasks/task_kanban.html"
    model = Task

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).select_related("project")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        context["columns"] = [
            ("todo", "À faire", qs.filter(status="todo")),
            ("in_progress", "En cours", qs.filter(status="in_progress")),
            ("waiting", "En attente", qs.filter(status="waiting")),
            ("done", "Terminée", qs.filter(status="done")),
        ]
        return context


class TaskDetailView(OwnerQuerySetMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"


class TaskCreateView(OwnerQuerySetMixin, AssignOwnerMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_message = "Tâche créée."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        project_id = self.request.GET.get("project")
        if project_id:
            initial["project"] = project_id
        return initial


class TaskUpdateView(OwnerQuerySetMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_message = "Tâche mise à jour."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TaskDeleteView(OwnerQuerySetMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Tâche supprimée.")
        return super().delete(request, *args, **kwargs)


class TaskStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, owner=request.user)
        status = request.POST.get("status")
        allowed = {choice[0] for choice in Task.STATUS_CHOICES}
        if status not in allowed:
            return JsonResponse({"ok": False, "error": "Statut invalide."}, status=400)
        task.status = status
        task.save(update_fields=["status", "updated_at"])
        return JsonResponse({"ok": True, "status": task.status})
