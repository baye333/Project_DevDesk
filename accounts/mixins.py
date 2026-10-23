from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerQuerySetMixin(LoginRequiredMixin):
    owner_field = "owner"

    def get_queryset(self):
        return super().get_queryset().filter(**{self.owner_field: self.request.user})


class AssignOwnerMixin(LoginRequiredMixin):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
