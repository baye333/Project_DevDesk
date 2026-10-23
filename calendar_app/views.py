import calendar
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timezone import make_aware
from django.views.generic import CreateView, DeleteView, DetailView, TemplateView, UpdateView

from accounts.mixins import AssignOwnerMixin, OwnerQuerySetMixin
from projects.models import Project
from tasks.models import Task
from .forms import EventForm
from .models import Event


def _month_matrix(year, month):
    cal = calendar.Calendar(firstweekday=0)
    return cal.monthdatescalendar(year, month)


class CalendarMonthView(OwnerQuerySetMixin, TemplateView):
    template_name = "calendar_app/month.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        year = int(self.request.GET.get("year", today.year))
        month = int(self.request.GET.get("month", today.month))
        if month < 1 or month > 12:
            month = today.month
        weeks = _month_matrix(year, month)
        start = datetime.combine(weeks[0][0], datetime.min.time())
        end = datetime.combine(weeks[-1][-1], datetime.max.time())
        start = make_aware(start)
        end = make_aware(end)

        events = Event.objects.filter(owner=self.request.user, start__lte=end, end__gte=start)
        tasks = Task.objects.filter(owner=self.request.user, due_date__range=(weeks[0][0], weeks[-1][-1]))
        projects = Project.objects.filter(
            owner=self.request.user, due_date__range=(weeks[0][0], weeks[-1][-1])
        )

        by_day = {}
        for event in events:
            day = timezone.localtime(event.start).date()
            by_day.setdefault(day, {"events": [], "tasks": [], "projects": []})
            by_day[day]["events"].append(event)
        for task in tasks:
            by_day.setdefault(task.due_date, {"events": [], "tasks": [], "projects": []})
            by_day[task.due_date]["tasks"].append(task)
        for project in projects:
            by_day.setdefault(project.due_date, {"events": [], "tasks": [], "projects": []})
            by_day[project.due_date]["projects"].append(project)

        prev_month = month - 1 or 12
        prev_year = year - 1 if month == 1 else year
        next_month = month + 1 if month < 12 else 1
        next_year = year + 1 if month == 12 else year

        context.update(
            {
                "year": year,
                "month": month,
                "month_name": calendar.month_name[month],
                "weeks": weeks,
                "by_day": by_day,
                "today": today,
                "prev_year": prev_year,
                "prev_month": prev_month,
                "next_year": next_year,
                "next_month": next_month,
            }
        )
        return context


class CalendarWeekView(OwnerQuerySetMixin, TemplateView):
    template_name = "calendar_app/week.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        raw = self.request.GET.get("start")
        if raw:
            start_date = datetime.strptime(raw, "%Y-%m-%d").date()
        else:
            start_date = today - timedelta(days=today.weekday())
        days = [start_date + timedelta(days=i) for i in range(7)]
        start_dt = make_aware(datetime.combine(days[0], datetime.min.time()))
        end_dt = make_aware(datetime.combine(days[-1], datetime.max.time()))
        events = Event.objects.filter(owner=self.request.user, start__lte=end_dt, end__gte=start_dt)
        tasks = Task.objects.filter(owner=self.request.user, due_date__range=(days[0], days[-1]))
        projects = Project.objects.filter(owner=self.request.user, due_date__range=(days[0], days[-1]))
        by_day = {day: {"events": [], "tasks": [], "projects": []} for day in days}
        for event in events:
            day = timezone.localtime(event.start).date()
            if day in by_day:
                by_day[day]["events"].append(event)
        for task in tasks:
            if task.due_date in by_day:
                by_day[task.due_date]["tasks"].append(task)
        for project in projects:
            if project.due_date in by_day:
                by_day[project.due_date]["projects"].append(project)
        context.update(
            {
                "days": days,
                "by_day": by_day,
                "prev_start": (days[0] - timedelta(days=7)).isoformat(),
                "next_start": (days[0] + timedelta(days=7)).isoformat(),
                "today": today,
            }
        )
        return context


class EventDetailView(OwnerQuerySetMixin, DetailView):
    model = Event
    template_name = "calendar_app/event_detail.html"


class EventCreateView(AssignOwnerMixin, SuccessMessageMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "calendar_app/event_form.html"
    success_message = "Événement créé."
    success_url = reverse_lazy("calendar_app:month")


class EventUpdateView(OwnerQuerySetMixin, SuccessMessageMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "calendar_app/event_form.html"
    success_message = "Événement mis à jour."
    success_url = reverse_lazy("calendar_app:month")


class EventDeleteView(OwnerQuerySetMixin, DeleteView):
    model = Event
    template_name = "calendar_app/event_confirm_delete.html"
    success_url = reverse_lazy("calendar_app:month")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Événement supprimé.")
        return super().delete(request, *args, **kwargs)
