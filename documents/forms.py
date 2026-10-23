from pathlib import Path

from django import forms
from django.conf import settings

from accounts.forms import StyledFormMixin
from projects.models import Project
from .models import Document


class DocumentForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Document
        fields = ("title", "category", "project", "file")

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["project"].queryset = Project.objects.filter(owner=user)
        self.fields["project"].required = False
        self._style()

    def clean_file(self):
        upload = self.cleaned_data.get("file")
        if not upload:
            return upload
        ext = Path(upload.name).suffix.lower().lstrip(".")
        if ext not in settings.ALLOWED_DOCUMENT_EXTENSIONS:
            raise forms.ValidationError(
                "Type de fichier non autorisé. Formats acceptés : PDF, DOCX, XLSX, PPTX et images."
            )
        if upload.size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError("Le fichier dépasse la taille maximale de 10 Mo.")
        return upload
