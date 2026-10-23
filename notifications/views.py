from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View

from .models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "notifications/list.html"
    context_object_name = "notifications"
    paginate_by = 20

    def get_queryset(self):
        return Notification.objects.filter(owner=self.request.user)


class NotificationReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        notif = get_object_or_404(Notification, pk=pk, owner=request.user)
        notif.is_read = True
        notif.save(update_fields=["is_read"])
        if notif.link:
            return redirect(notif.link)
        return redirect("notifications:list")


class NotificationReadAllView(LoginRequiredMixin, View):
    def post(self, request):
        Notification.objects.filter(owner=request.user, is_read=False).update(is_read=True)
        return redirect("notifications:list")
