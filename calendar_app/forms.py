from django import forms

from accounts.forms import StyledFormMixin
from .models import Event


class EventForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ("title", "description", "start", "end", "all_day")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "start": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("start", "end"):
            value = getattr(self.instance, name, None)
            if value:
                self.initial[name] = value.strftime("%Y-%m-%dT%H:%M")
        self._style()

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("start")
        end = cleaned.get("end")
        if start and end and end < start:
            raise forms.ValidationError("La date de fin doit être postérieure au début.")
        return cleaned
