from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from accounts.mixins import AssignOwnerMixin, OwnerQuerySetMixin
from .forms import ProjectForm
from .models import Project


class ProjectListView(OwnerQuerySetMixin, ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(title__icontains=q)
        return qs


class ProjectDetailView(OwnerQuerySetMixin, DetailView):
    model = Project
    template_name = "projects/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        context["project_tasks"] = project.tasks.filter(owner=self.request.user)
        context["project_notes"] = project.notes.filter(owner=self.request.user)
        context["project_docs"] = project.documents.filter(owner=self.request.user)
        return context


class ProjectCreateView(OwnerQuerySetMixin, AssignOwnerMixin, SuccessMessageMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    success_message = "Projet créé."


class ProjectUpdateView(OwnerQuerySetMixin, SuccessMessageMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    success_message = "Projet mis à jour."


class ProjectDeleteView(OwnerQuerySetMixin, DeleteView):
    model = Project
    template_name = "projects/project_confirm_delete.html"
    success_url = reverse_lazy("projects:list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Projet supprimé.")
        return super().delete(request, *args, **kwargs)
