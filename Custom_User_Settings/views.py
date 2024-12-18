from django.shortcuts import render
from django.views import generic

from Custom_User_Settings.models import Custom_User_Settings
from user_profile import mixins as user_mixins


# Create your views here.
class CreateSettingsView(user_mixins.LoginRequiredMixin, generic.CreateView):
    template_name = "settings_Template.html"

    def get(self, request):
        user_settings, created = Custom_User_Settings.objects.get_or_create(
            user_settings=request.user
        )
        context = {
            "dark_mode": user_settings.dark_mode if user_settings else False,
            "retain_last_used_options": (
                user_settings.retain_last_used_options if user_settings else False
            ),
            "theme": (user_settings.theme if user_settings else "galactic_blood"),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user_settings, created = Custom_User_Settings.objects.get_or_create(
            user_settings=request.user
        )
        post_request = request.POST
        dark_mode = post_request.get("darkMode") == "on"  # Checkbox value
        retain_last_used_options = post_request.get("retainLastUsedOptions") == "on"
        theme = request.POST.get("theme")
        user_settings.dark_mode = dark_mode
        user_settings.retain_last_used_options = retain_last_used_options
        if theme:
            user_settings.theme = theme
        user_settings.save()

        # Update context with new settings
        context = {
            "dark_mode": dark_mode,
            "retain_last_used_options": retain_last_used_options,
            "theme": theme,
        }
        return render(request, self.template_name, context)
