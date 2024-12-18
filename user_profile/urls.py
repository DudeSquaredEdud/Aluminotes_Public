"""User profile app URL."""

from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = "user_profile"

urlpatterns = [
    path("profile/", views.UserProfileDetailView.as_view(), name="profile_detail"),
    path(
        "profile/update/", views.UserProfileDetailView.as_view(), name="profile_update"
    ),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('customer-portal/', views.CreateCustomerPortalSessionView.as_view(), name='customer_portal'),
    path('webhook/stripe/', csrf_exempt(views.StripeWebhookView.as_view()), name='stripe_webhook'),
]
