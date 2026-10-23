from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from accounts.mixins import AssignOwnerMixin, OwnerQuerySetMixin
from .forms import LearningGoalForm, LearningResourceForm, LearningSessionForm, SkillForm
from .models import LearningGoal, LearningResource, LearningSession, Skill


class LearningHomeView(OwnerQuerySetMixin, TemplateView):
    template_name = "learning/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["skills"] = Skill.objects.filter(owner=user)
        context["goals"] = LearningGoal.objects.filter(owner=user)
        context["sessions"] = LearningSession.objects.filter(owner=user)[:10]
        context["resources"] = LearningResource.objects.filter(owner=user)[:10]
        return context


class SkillCreateView(AssignOwnerMixin, SuccessMessageMixin, CreateView):
    model = Skill
    form_class = SkillForm
    template_name = "learning/skill_form.html"
    success_url = reverse_lazy("learning:home")
    success_message = "Compétence ajoutée."


class SkillUpdateView(OwnerQuerySetMixin, SuccessMessageMixin, UpdateView):
    model = Skill
    form_class = SkillForm
    template_name = "learning/skill_form.html"
    success_url = reverse_lazy("learning:home")
    success_message = "Compétence mise à jour."


class SkillDeleteView(OwnerQuerySetMixin, DeleteView):
    model = Skill
    template_name = "learning/confirm_delete.html"
    success_url = reverse_lazy("learning:home")


class GoalListView(OwnerQuerySetMixin, ListView):
    model = LearningGoal
    template_name = "learning/goal_list.html"
    context_object_name = "goals"


class GoalDetailView(OwnerQuerySetMixin, DetailView):
    model = LearningGoal
    template_name = "learning/goal_detail.html"


class GoalCreateView(AssignOwnerMixin, SuccessMessageMixin, CreateView):
    model = LearningGoal
    form_class = LearningGoalForm
    template_name = "learning/goal_form.html"
    success_message = "Objectif créé."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class GoalUpdateView(OwnerQuerySetMixin, SuccessMessageMixin, UpdateView):
    model = LearningGoal
    form_class = LearningGoalForm
    template_name = "learning/goal_form.html"
    success_message = "Objectif mis à jour."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class GoalDeleteView(OwnerQuerySetMixin, DeleteView):
    model = LearningGoal
    template_name = "learning/confirm_delete.html"
    success_url = reverse_lazy("learning:home")


class SessionCreateView(AssignOwnerMixin, SuccessMessageMixin, CreateView):
    model = LearningSession
    form_class = LearningSessionForm
    template_name = "learning/session_form.html"
    success_url = reverse_lazy("learning:home")
    success_message = "Session enregistrée."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class SessionDeleteView(OwnerQuerySetMixin, DeleteView):
    model = LearningSession
    template_name = "learning/confirm_delete.html"
    success_url = reverse_lazy("learning:home")


class ResourceCreateView(AssignOwnerMixin, SuccessMessageMixin, CreateView):
    model = LearningResource
    form_class = LearningResourceForm
    template_name = "learning/resource_form.html"
    success_url = reverse_lazy("learning:home")
    success_message = "Ressource ajoutée."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ResourceDeleteView(OwnerQuerySetMixin, DeleteView):
    model = LearningResource
    template_name = "learning/confirm_delete.html"
    success_url = reverse_lazy("learning:home")
