from django import forms

from accounts.forms import StyledFormMixin
from projects.models import Project
from .models import Task


class TaskForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ("title", "description", "project", "priority", "status", "due_date")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["project"].queryset = Project.objects.filter(owner=user)
        self.fields["project"].required = False
        self._style()


class TaskFilterForm(StyledFormMixin, forms.Form):
    q = forms.CharField(required=False, label="Recherche")
    status = forms.ChoiceField(
        required=False, choices=(("", "Tous les statuts"),) + Task.STATUS_CHOICES
    )
    priority = forms.ChoiceField(
        required=False, choices=(("", "Toutes les priorités"),) + Task.PRIORITY_CHOICES
    )
    project = forms.ModelChoiceField(required=False, queryset=Project.objects.none())
    sort = forms.ChoiceField(
        required=False,
        choices=(
            ("-updated_at", "Récents"),
            ("due_date", "Échéance"),
            ("priority", "Priorité"),
            ("title", "Titre"),
        ),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["project"].queryset = Project.objects.filter(owner=user)
        self._style()
