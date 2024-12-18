"""User Profile Forms."""

from django import forms

from . import models


class UserProfileUpdateForm(forms.ModelForm):
    """User profile change view."""

    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)

    class Meta:
        """Meta class."""

        model = models.UserProfile
        fields = ["first_name", "last_name", "picture"]
