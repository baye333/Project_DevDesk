from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "status", "priority", "progress", "due_date")
    list_filter = ("status", "priority", "category")
    search_fields = ("title", "technologies")
