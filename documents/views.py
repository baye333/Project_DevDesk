from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import FileResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from accounts.mixins import AssignOwnerMixin, OwnerQuerySetMixin
from .forms import DocumentForm
from .models import Document


class DocumentListView(OwnerQuerySetMixin, ListView):
    model = Document
    template_name = "documents/document_list.html"
    context_object_name = "documents"
    paginate_by = 15

    def get_queryset(self):
        qs = super().get_queryset().select_related("project")
        category = self.request.GET.get("category")
        q = self.request.GET.get("q")
        if category:
            qs = qs.filter(category=category)
        if q:
            qs = qs.filter(title__icontains=q)
        return qs


class DocumentDetailView(OwnerQuerySetMixin, DetailView):
    model = Document
    template_name = "documents/document_detail.html"


class DocumentCreateView(AssignOwnerMixin, SuccessMessageMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = "documents/document_form.html"
    success_message = "Document téléversé."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        upload = form.cleaned_data.get("file")
        if upload:
            form.instance.original_name = upload.name
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get("project"):
            initial["project"] = self.request.GET["project"]
        return initial


class DocumentDeleteView(OwnerQuerySetMixin, DeleteView):
    model = Document
    template_name = "documents/document_confirm_delete.html"
    success_url = reverse_lazy("documents:list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Document supprimé.")
        return super().delete(request, *args, **kwargs)


class DocumentDownloadView(OwnerQuerySetMixin, DetailView):
    model = Document

    def get(self, request, *args, **kwargs):
        document = self.get_object()
        if not document.file:
            raise Http404()
        filename = document.original_name or document.file.name
        return FileResponse(document.file.open("rb"), as_attachment=True, filename=filename)
