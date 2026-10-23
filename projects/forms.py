from django import forms

from accounts.forms import StyledFormMixin
from .models import Project


class ProjectForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            "title",
            "description",
            "category",
            "technologies",
            "priority",
            "status",
            "progress",
            "due_date",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "progress": forms.NumberInput(attrs={"min": 0, "max": 100}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()
