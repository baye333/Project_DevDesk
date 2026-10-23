from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import LoginForm, ProfileForm, RegisterForm, StyledPasswordChangeForm
from .models import Profile


class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("dashboard:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard:home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Compte créé. Bienvenue sur DevDesk.")
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


class UserPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    form_class = StyledPasswordChangeForm
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        messages.success(self.request, "Mot de passe mis à jour.")
        return super().form_valid(form)


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user, defaults={"display_name": request.user.get_username()}
    )
    return render(request, "accounts/profile.html", {"profile": profile})


@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user, defaults={"display_name": request.user.get_username()}
    )
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=profile, user=request.user)
    return render(request, "accounts/profile_form.html", {"form": form})


@login_required
def theme_toggle(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    profile.theme = "light" if profile.theme == "dark" else "dark"
    profile.save(update_fields=["theme"])
    next_url = request.POST.get("next") or request.GET.get("next") or request.META.get("HTTP_REFERER") or "/"
    return redirect(next_url)


@login_required
def avatar_download(request):
    profile = getattr(request.user, "profile", None)
    if not profile or not profile.avatar:
        raise Http404()
    return FileResponse(profile.avatar.open("rb"), as_attachment=False)
