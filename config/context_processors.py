from notifications.models import Notification


def ui_context(request):
    theme = "dark"
    unread_count = 0
    if request.user.is_authenticated:
        profile = getattr(request.user, "profile", None)
        if profile and profile.theme:
            theme = profile.theme
        unread_count = Notification.objects.filter(
            owner=request.user, is_read=False
        ).count()
    else:
        theme = request.session.get("theme", "dark")
    return {
        "ui_theme": theme,
        "unread_notifications": unread_count,
    }
