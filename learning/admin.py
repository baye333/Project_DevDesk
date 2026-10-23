from django.contrib import admin

from .models import LearningGoal, LearningResource, LearningSession, Skill

admin.site.register(Skill)
admin.site.register(LearningGoal)
admin.site.register(LearningSession)
admin.site.register(LearningResource)
