from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("accounts/", include("accounts.urls")),
    path("projects/", include("projects.urls")),
    path("tasks/", include("tasks.urls")),
    path("notes/", include("notes.urls")),
    path("learning/", include("learning.urls")),
    path("documents/", include("documents.urls")),
    path("calendar/", include("calendar_app.urls")),
    path("notifications/", include("notifications.urls")),
]
