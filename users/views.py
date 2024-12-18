"""Accounts view."""

from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CustomUserCreationForm
from users.models import CustomUser

from django.contrib import messages

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token


class SignUpView(CreateView):
    """User registration view."""

    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "allauth/account/signup.html"
    success_url = reverse_lazy("/toolpage_app")
    extra_context = {"title_text": "Sign Up", "button_text": "Register"}

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.isactive = False
        user.save()
        mail_subject = "Activate your user account."
        message = render_to_string(
            "activate_account.html",
            {
                "user": user.username,
                "domain": get_current_site(self.request).domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
                "protocol": "https" if self.request.is_secure() else "http",
            },
        )
        email = EmailMessage(mail_subject, message, to=[user.email])
        if not (email.send()):
            messages.error(
                self.request,
                f"Problem sending confirmation email to {user.email}, check if you typed it correctly.",
            )
        else:
            messages.success(
                self.request,
                "Sign up successful. Please check your email to activate your account.",
            )

        # Redirect to login page
        return redirect(self.get_success_url())


def activate(request, uidb64, token):
    User = CustomUser
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            request,
            "Thank you for your email confirmation. Now you can login your account.",
        )
        return redirect("login")
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect("homepage")
