"""Accounts app URL Configuration."""

from django.urls import path

from users import views as users_views
from . import views

app_name = "users"

urlpatterns = [
    path(
        "signup/",
        users_views.SignUpView.as_view(success_url="/toolpage_app/"),
        name="signup",
    ),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
]
