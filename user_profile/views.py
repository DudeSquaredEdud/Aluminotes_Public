import stripe
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View, generic
from django.views.decorators.csrf import csrf_protect

from .forms import UserProfileUpdateForm
from .models import UserProfile


class UserProfileDetailView(LoginRequiredMixin, generic.DetailView):
    """Profile detail and update view."""

    model = UserProfile
    template_name = "user_profile/userprofile_detail.html"
    slug_field = None
    slug_url_kwarg = ""

    def get_object(self, queryset=None):
        """Retrieve the UserProfile of the current user."""
        return self.model.objects.get(custom_user=self.request.user)

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        """Handle form submission for updating user profile or deleting account."""
        user_profile = self.get_object()

        if "action" in request.POST:
            if request.POST.get("action") == "confirm-delete":
                if user_profile.custom_user != request.user:
                    # Just in case -- prevent other users from deleting your account
                    raise PermissionDenied("Cannot delete another user's profile.")
                user_profile.custom_user.delete()  # Delete the custom user
                logout(request)  # Log out the user
                return redirect("home")  # Redirect to home page

        form = UserProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.custom_user = self.request.user
            user_profile.save()
            request.user.first_name = form.cleaned_data["first_name"]
            request.user.last_name = form.cleaned_data["last_name"]
            request.user.save()
            return redirect("user_profile:profile_detail")
        return self.get(request, form=form)

    def get(self, request, *args, **kwargs):
        """Render the profile detail and update form."""
        user_profile = self.get_object()
        form = UserProfileUpdateForm(
            instance=user_profile,
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
            },
        )
        return render(
            request, self.template_name, {"form": form, "user_profile": user_profile}
        )

def delete_account(request):
    # Get the user profile
    user_profile = request.user.userprofile
    customer_id = user_profile.stripe_customer_id

    if customer_id:
        # Cancel all subscriptions for the customer
        subscriptions = stripe.Subscription.list(customer=customer_id)
        for subscription in subscriptions.auto_paging_iter():
            stripe.Subscription.delete(subscription.id)

        # Delete the Stripe customer
        stripe.Customer.delete(customer_id)

    # Delete the user profile and user account
    request.user.delete()

    # Redirect to home or another page
    return redirect('home')

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = "http://127.0.0.1:8000"

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1PsZjPCwhdqZcwfy8lY4EFxC',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN + reverse('user_profile:profile_detail'),
            cancel_url=YOUR_DOMAIN + reverse('user_profile:profile_detail'),
            metadata={
                'user_id': request.user.id,  # Storing the user's ID in metadata
            }
        )

        return JsonResponse({
            'id': checkout_session.id,
            'checkout_url': checkout_session.url
        })

class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            # Invalid signature
            return HttpResponse(status=400)

        # Handle checkout session event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            # Update the user's profile to Premium
            handle_checkout_session(session)

        # Handle subscription updated event
        if event['type'] == 'customer.subscription.updated':
            subscription = event['data']['object']  # Subscription object
            handle_subscription_update(subscription)

        # Handle subscription deletion or payment failure events
        if event['type'] == 'customer.subscription.deleted':
            subscription = event['data']['object']  # Contains the subscription object
            handle_subscription_cancellation(subscription)

        elif event['type'] == 'invoice.payment_failed':
            invoice = event['data']['object']  # Contains the invoice object
            handle_payment_failure(invoice)

        return HttpResponse(status=200)

def handle_checkout_session(session):
    # You can retrieve the user information from session['metadata'] if you stored it when creating the session
    # For example, assuming you stored the user ID in metadata:
    user_id = session.get('metadata', {}).get('user_id')
    customer_id = session.get('customer')

    # Debugging print statements
    print(f"Received Stripe session: {session}")
    print(f"Extracted user_id from metadata: {user_id}")

    if user_id:
        try:
            # Retrieve the corresponding UserProfile
            user_profile = UserProfile.objects.get(custom_user__id=user_id)
            print(f"Found UserProfile: {user_profile}")

            # Update the UserProfile to Premium
            user_profile.user_type = UserProfile.UserType.PREMIUM
            # Store the Stripe customer ID in the user's profile
            user_profile.stripe_customer_id = customer_id
            user_profile.save()
            print(f"Updated UserProfile to PREMIUM for user_id: {user_id}")
            print(f"Updated UserProfile with Stripe customer_id: {customer_id} for user_id: {user_id}")

        except UserProfile.DoesNotExist:
            # Print an error if the UserProfile does not exist
            print(f"Error: UserProfile not found for user_id: {user_id}")
    else:
        # Print an error if user_id is not found in the metadata
        print("Error: No user_id found in session metadata")

def handle_subscription_cancellation(subscription):
    # Retrieve the user ID from metadata stored during checkout session creation
    customer_id = subscription.get('customer')

    # Find the corresponding user profile based on the Stripe customer ID
    try:
        user_profile = UserProfile.objects.get(stripe_customer_id=customer_id)
        print(f"Found UserProfile: {user_profile}")
        # Update the user type to "Free"
        user_profile.user_type = UserProfile.UserType.FREE
        user_profile.save()

        print(f"Updated UserProfile to FREE for customer_id: {customer_id}")
    except UserProfile.DoesNotExist:
        print(f"UserProfile not found for customer_id: {customer_id}")

def handle_subscription_update(subscription):
    # Get the user ID from metadata (if stored)
    customer_id = subscription.get('customer')
    try:
        # Find the user profile with the matching user ID
        user_profile = UserProfile.objects.get(stripe_customer_id=customer_id)
        print(f"Found UserProfile: {user_profile}")

        # Get the subscription status & data
        subscription_data = subscription.get('items', {}).get('data', [])
        status = subscription.get('status')

        # Get Product ID
        for item in subscription_data:
            plan = item.get('plan', {})
            product_id = plan.get('product')

        print(f"PRODUCT: {product_id}")

        # Update user type based on subscription status
        if product_id == 'prod_Qk3r1jtusnFf8h':
            if status == 'active':
                user_profile.user_type = UserProfile.UserType.PREMIUM
        elif product_id == 'prod_QqSKjOlNpcSDdW':
            if status == 'active':
                user_profile.user_type = UserProfile.UserType.FREE

        user_profile.save()

        print(f"Updated UserProfile to {user_profile.user_type} for UserProfile: {user_profile}")
    except UserProfile.DoesNotExist:
        print(f"UserProfile not found for customer_id: {customer_id}")


def handle_payment_failure(invoice):
    customer_id = invoice.get('customer')

    try:
        user_profile = UserProfile.objects.get(stripe_customer_id=customer_id)
        # You could handle any custom logic here, such as sending reminders or warnings
        # Update the user type to "Free"
        user_profile.user_type = UserProfile.UserType.FREE
        user_profile.save()
        print(f"Payment failed for user: {user_profile.custom_user.email}")
    except UserProfile.DoesNotExist:
        print(f"UserProfile not found for customer_id: {customer_id}")

class CreateCustomerPortalSessionView(View):
    def post(self, request, *args, **kwargs):
        user_profile = request.user.userprofile

        # Ensure the user has a Stripe Customer ID
        # if not user_profile.stripe_customer_id:
            # return redirect("some_error_page")  # Handle error as needed

        # Create a customer portal session
        session = stripe.billing_portal.Session.create(
            customer=user_profile.stripe_customer_id,
            return_url=request.build_absolute_uri('/accounts/profile/'),
        )

        # Redirect the user to the portal session URL
        return redirect(session.url)

