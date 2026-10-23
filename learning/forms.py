from django import forms

from accounts.forms import StyledFormMixin
from .models import LearningGoal, LearningResource, LearningSession, Skill


class SkillForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Skill
        fields = ("name", "category", "level", "progress")
        widgets = {"progress": forms.NumberInput(attrs={"min": 0, "max": 100})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()


class LearningGoalForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = LearningGoal
        fields = ("title", "skill", "description", "deadline", "progress", "status")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "deadline": forms.DateInput(attrs={"type": "date"}),
            "progress": forms.NumberInput(attrs={"min": 0, "max": 100}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["skill"].queryset = Skill.objects.filter(owner=user)
        self.fields["skill"].required = False
        self._style()


class LearningSessionForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = LearningSession
        fields = ("title", "goal", "skill", "duration_minutes", "date", "notes")
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["goal"].queryset = LearningGoal.objects.filter(owner=user)
            self.fields["skill"].queryset = Skill.objects.filter(owner=user)
        self.fields["goal"].required = False
        self.fields["skill"].required = False
        self._style()


class LearningResourceForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = LearningResource
        fields = ("title", "url", "resource_type", "goal", "skill")

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["goal"].queryset = LearningGoal.objects.filter(owner=user)
            self.fields["skill"].queryset = Skill.objects.filter(owner=user)
        self.fields["goal"].required = False
        self.fields["skill"].required = False
        self._style()
