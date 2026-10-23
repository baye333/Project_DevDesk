from django.urls import path

from . import views

app_name = "calendar_app"

urlpatterns = [
    path("", views.CalendarMonthView.as_view(), name="month"),
    path("week/", views.CalendarWeekView.as_view(), name="week"),
    path("events/create/", views.EventCreateView.as_view(), name="create"),
    path("events/<int:pk>/", views.EventDetailView.as_view(), name="detail"),
    path("events/<int:pk>/edit/", views.EventUpdateView.as_view(), name="update"),
    path("events/<int:pk>/delete/", views.EventDeleteView.as_view(), name="delete"),
]
