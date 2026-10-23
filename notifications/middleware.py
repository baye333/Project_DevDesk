from .services import sync_deadline_notifications


class DeadlineNotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_sync = request.session.get("notif_sync_date")
            from django.utils import timezone

            today = str(timezone.localdate())
            if last_sync != today:
                sync_deadline_notifications(request.user)
                request.session["notif_sync_date"] = today
        return self.get_response(request)
