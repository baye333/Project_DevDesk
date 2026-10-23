from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("password/", views.UserPasswordChangeView.as_view(), name="password_change"),
    path("theme/", views.theme_toggle, name="theme_toggle"),
    path("avatar/", views.avatar_download, name="avatar"),
]
