from django.urls import path
from Custom_User_Settings import views

app_name = "Custom_User_Settings"

urlpatterns = [
    path("settings/", views.CreateSettingsView.as_view(), name="settings"),
]
