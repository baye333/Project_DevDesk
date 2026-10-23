from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from accounts.mixins import AssignOwnerMixin, OwnerQuerySetMixin
from .forms import NoteForm
from .models import Note


class NoteListView(OwnerQuerySetMixin, ListView):
    model = Note
    template_name = "notes/note_list.html"
    context_object_name = "notes"
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset().select_related("project")
        q = self.request.GET.get("q")
        category = self.request.GET.get("category")
        fav = self.request.GET.get("favorite")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(tags__icontains=q))
        if category:
            qs = qs.filter(category=category)
        if fav == "1":
            qs = qs.filter(is_favorite=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Note.CATEGORY_CHOICES
        return context


class NoteDetailView(OwnerQuerySetMixin, DetailView):
    model = Note
    template_name = "notes/note_detail.html"


class NoteCreateView(OwnerQuerySetMixin, AssignOwnerMixin, SuccessMessageMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"
    success_message = "Note enregistrée."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get("project"):
            initial["project"] = self.request.GET["project"]
        return initial


class NoteUpdateView(OwnerQuerySetMixin, SuccessMessageMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "notes/note_form.html"
    success_message = "Note mise à jour."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class NoteDeleteView(OwnerQuerySetMixin, DeleteView):
    model = Note
    template_name = "notes/note_confirm_delete.html"
    success_url = reverse_lazy("notes:list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Note supprimée.")
        return super().delete(request, *args, **kwargs)
