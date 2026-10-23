from django import forms

from accounts.forms import StyledFormMixin
from projects.models import Project
from .models import Note


class NoteForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Note
        fields = ("title", "content", "category", "tags", "project", "is_favorite")
        widgets = {
            "content": forms.Textarea(attrs={"rows": 12, "class": "font-monospace"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["project"].queryset = Project.objects.filter(owner=user)
        self.fields["project"].required = False
        self._style()
