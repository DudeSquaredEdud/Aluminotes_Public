"""Forms for accounts app."""

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Registration form."""

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "type": "password",
                "placeholder": "Password",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-lg",
                "type": "password",
                "placeholder": "Re-Enter Password",
            }
        ),
    )

    class Meta:
        """Meta class."""

        model = CustomUser
        fields = ("first_name", "last_name", "email", "password1", "password2")
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "First Name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": "Last Name",
                }
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control form-control-lg", "placeholder": "Email"}
            ),
        }


class CustomUserChangeForm(UserChangeForm):
    """User profile change view."""

    class Meta:
        """Meta class."""

        model = CustomUser
        fields = ("first_name", "last_name", "email")
