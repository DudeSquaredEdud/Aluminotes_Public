"""django_project URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/

Examples
--------
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView

from users import views as users_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", TemplateView.as_view(template_name="home.html"), name="home"),
    path("", TemplateView.as_view(template_name="home.html"), name="home2"),
    path(
        "team/",
        TemplateView.as_view(template_name="team.html"),
        name="team",
    ),
    path(
        "about/",
        TemplateView.as_view(template_name="about.html"),
        name="about",
    ),
    path(
        "terms/",
        TemplateView.as_view(template_name="terms_conditions.html"),
        name="terms",
    ),
    path(
        "feedback/",
        TemplateView.as_view(template_name="feedback.html"),
        name="feedback",
    ),
    path(
        "pricing/",
        TemplateView.as_view(template_name="pricing.html"),
        name="pricing",
    ),
    path("accounts/", include("users.urls", namespace="users")),
    path("accounts/", include("user_profile.urls")),
    path("", include("Custom_User_Settings.urls")),
    path("", include("SavedUserTemplates.urls")),
]

urlpatterns += [
    path(
        "accounts/password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="allauth/account/password_change.html"
        ),
        name="password_change",
    ),
    path(
        "accounts/password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="allauth/account/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="allauth/account/login.html"),
        name="login",
    ),
    path(
        "accounts/signup/",
        users_views.SignUpView.as_view(template_name="allauth/account/signup.html"),
        name="signup",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(template_name="allauth/account/logout.html"),
        name="logout",
    ),
    path(
        "accounts/password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="allauth/account/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "accounts/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="allauth/account/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="allauth/account/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("", include("toolpage.urls")),
    path("", include("Custom_User_Settings.urls", namespace="list-settings")),
]

urlpatterns += [
    path("", include("SavedUserTemplates.urls", namespace="SavedUserTemplate")),
]

# Allauth
urlpatterns += [
    path("accounts/", include("allauth.urls")),
]
