from django.contrib import admin

from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "category", "is_favorite", "updated_at")
    list_filter = ("category", "is_favorite")
    search_fields = ("title", "tags")
