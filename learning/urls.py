from django.urls import path

from . import views

app_name = "learning"

urlpatterns = [
    path("", views.LearningHomeView.as_view(), name="home"),
    path("skills/create/", views.SkillCreateView.as_view(), name="skill_create"),
    path("skills/<int:pk>/edit/", views.SkillUpdateView.as_view(), name="skill_update"),
    path("skills/<int:pk>/delete/", views.SkillDeleteView.as_view(), name="skill_delete"),
    path("goals/", views.GoalListView.as_view(), name="goal_list"),
    path("goals/create/", views.GoalCreateView.as_view(), name="goal_create"),
    path("goals/<int:pk>/", views.GoalDetailView.as_view(), name="goal_detail"),
    path("goals/<int:pk>/edit/", views.GoalUpdateView.as_view(), name="goal_update"),
    path("goals/<int:pk>/delete/", views.GoalDeleteView.as_view(), name="goal_delete"),
    path("sessions/create/", views.SessionCreateView.as_view(), name="session_create"),
    path("sessions/<int:pk>/delete/", views.SessionDeleteView.as_view(), name="session_delete"),
    path("resources/create/", views.ResourceCreateView.as_view(), name="resource_create"),
    path("resources/<int:pk>/delete/", views.ResourceDeleteView.as_view(), name="resource_delete"),
]
