import sys

sys.path.append("..")  # Adds higher directory to python modules path.
from user_profile.models import UserProfile

from django.test import TestCase

from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import SavedUserTemplate
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from . import models
from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin


class SavedUserTemplateModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User = get_user_model()
        cls.user = User.objects.create_user(
            email="testuser@example.com",  # Use the email as the primary identifier if that's what your model uses
            password="testpass",
            # Include any other required fields according to your CustomUser model
        )
        cls.saved_user_template = SavedUserTemplate.objects.create(
            author=cls.user,
            name_of_template="Test Template",
            summary=True,
            formal=False,
            # Set other fields if necessary
        )

    def test_saved_user_template_creation(self):
        # Test that the SavedUserTemplate instance has been created successfully.
        self.assertIsInstance(self.saved_user_template, SavedUserTemplate)

    def test_saved_user_template_fields(self):
        # Test that the fields of the SavedUserTemplate instance contain the correct values.
        self.assertEqual(self.saved_user_template.author, self.user)
        self.assertEqual(self.saved_user_template.name_of_template, "Test Template")
        self.assertTrue(self.saved_user_template.summary)
        self.assertFalse(self.saved_user_template.formal)
        # Add assertions for other fields if necessary

    def test_saved_user_template_str(self):
        # Test the string representation of the SavedUserTemplate instance.
        self.assertEqual(str(self.saved_user_template), "Test Template")


from django.test import TestCase, override_settings


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class CreateTemplateViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        User = get_user_model()
        cls.premium_user = User.objects.create_user(
            email="premiumuser@example.com",
            password="testpass",
        )
        # Assuming the signal creates the UserProfile, you can access it like this:
        cls.premium_profile = UserProfile.objects.get(custom_user=cls.premium_user)
        # Update the profile to set it as premium
        cls.premium_profile.user_type = UserProfile.UserType.PREMIUM
        cls.premium_profile.save()

        cls.non_premium_user = User.objects.create_user(
            email="nonpremiumuser@example.com",
            password="testpass",
        )
        cls.non_premium_profile = UserProfile.objects.get(
            custom_user=cls.non_premium_user
        )
        # Update the profile to set it as non-premium if necessary
        cls.non_premium_profile.user_type = UserProfile.UserType.FREE
        cls.non_premium_profile.save()

        cls.client = Client()

    def test_access_to_premium_user(self):
        # Make sure the user is logged in and recognized as premium
        login = self.client.login(email="premiumuser@example.com", password="testpass")
        self.assertTrue(
            login, "User should be logged in"
        )  # Confirm that the login was successful
        # Then access the view
        response = self.client.get(reverse("SavedUserTemplates:create-template"))
        # Make sure the user is not redirected
        self.assertEqual(response.status_code, 200)

    def test_access_to_non_premium_user(self):
        # Non-premium user should be redirected or get a forbidden response
        self.client.login(email="nonpremiumuser@example.com", password="testpass")
        response = self.client.get(reverse("SavedUserTemplates:create-template"))
        self.assertNotEqual(response.status_code, 200)

    def test_form_valid_and_redirect(self):
        # Ensure the user is logged in and recognized as premium
        self.client.login(email="premiumuser@example.com", password="testpass")
        form_data = {
            "name_of_template": "Test Template",
            "summary": True,
            "formal": False,
            # Make sure all required fields are included
        }
        response = self.client.post(
            reverse("SavedUserTemplates:create-template"), form_data
        )
        self.assertEqual(
            response.status_code,
            302,
            "The response should be a redirect on successful form submission.",
        )
        # Check if the object has been created
        self.assertTrue(
            models.SavedUserTemplate.objects.filter(
                name_of_template="Test Template"
            ).exists(),
            "SavedUserTemplate object should exist after POST.",
        )
        # If object creation is successful, you can also check if the user has been set as the author correctly
        template = models.SavedUserTemplate.objects.get(
            name_of_template="Test Template"
        )
        self.assertEqual(template.author, self.premium_user)

    def test_template_creation(self):
        # Log in as the premium user
        self.client.login(email="premiumuser@example.com", password="testpass")

        # Ensure that the user is recognized as premium (i.e., has a profile with the correct user_type)
        user_profile = UserProfile.objects.get(custom_user=self.premium_user)
        self.assertEqual(user_profile.user_type, UserProfile.UserType.PREMIUM)

        # Provide complete form data
        form_data = {
            "name_of_template": "Another Test Template",
            "summary": False,
            "formal": True,
            # ... rest of the required fields
        }

        # Post the form data and check the response
        response = self.client.post(
            reverse("SavedUserTemplates:create-template"), form_data
        )

        # Check if the template was created
        self.assertEqual(
            response.status_code,
            302,
            "Should redirect to success URL after form is valid.",
        )
        self.assertTrue(
            SavedUserTemplate.objects.filter(
                name_of_template="Another Test Template"
            ).exists(),
            "SavedUserTemplate should be created.",
        )

        # Check if the author was set correctly
        template = SavedUserTemplate.objects.get(
            name_of_template="Another Test Template"
        )
        self.assertEqual(template.author, self.premium_user)


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class TemplateListViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a premium user
        cls.premium_user = CustomUser.objects.create_user(
            email="premiumuser@example.com", password="testpass123"
        )
        # The UserProfile for this user is automatically created by the post_save signal,
        # so we can retrieve it and update the user_type
        cls.premium_user_profile = UserProfile.objects.get(custom_user=cls.premium_user)
        cls.premium_user_profile.user_type = UserProfile.UserType.PREMIUM
        cls.premium_user_profile.save()

        # Create a non-premium user
        cls.non_premium_user = CustomUser.objects.create_user(
            email="nonpremiumuser@example.com", password="testpass123"
        )
        # Similarly, update the UserProfile for the non-premium user
        cls.non_premium_user_profile = UserProfile.objects.get(
            custom_user=cls.non_premium_user
        )
        cls.non_premium_user_profile.user_type = UserProfile.UserType.FREE
        cls.non_premium_user_profile.save()

        # Create templates for the premium user
        cls.template1 = SavedUserTemplate.objects.create(
            author=cls.premium_user, name_of_template="Premium Template 1"
        )
        cls.template2 = SavedUserTemplate.objects.create(
            author=cls.premium_user, name_of_template="Premium Template 2"
        )

        # Create a template for the non-premium user
        cls.template3 = SavedUserTemplate.objects.create(
            author=cls.non_premium_user, name_of_template="Non-Premium Template"
        )

        cls.client = Client()

    def test_list_view_premium_user(self):
        self.client.login(email="premiumuser@example.com", password="testpass123")
        response = self.client.get(
            reverse("SavedUserTemplates:list-templates")
        )  # Adjust the 'template_list' to the correct url name
        self.assertEqual(response.status_code, 200)
        # Check that only the premium user's templates are listed
        self.assertEqual(len(response.context["object_list"]), 2)
        self.assertIn(self.template1, response.context["object_list"])
        self.assertIn(self.template2, response.context["object_list"])
        self.assertNotIn(self.template3, response.context["object_list"])

    def test_list_view_non_premium_user(self):
        self.client.login(email="nonpremiumuser@example.com", password="testpass123")
        response = self.client.get(
            reverse("SavedUserTemplates:list-templates")
        )  # Adjust the 'template_list' to the correct url name
        # Assuming that the non-premium user is redirected or forbidden access
        self.assertNotEqual(response.status_code, 200)

    def test_list_view_not_logged_in(self):
        response = self.client.get(
            reverse("SavedUserTemplates:list-templates")
        )  # Adjust the 'template_list' to the correct url name
        # Assuming that anonymous users are redirected to the login page
        self.assertEqual(response.status_code, 302)


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class TemplateDetailViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a premium user
        cls.premium_user = CustomUser.objects.create_user(
            email="premium@example.com",
            password="testpass123",
        )
        # The UserProfile for this user is automatically created by the post_save signal,
        # so we can retrieve it and update the user_type
        cls.premium_user_profile = UserProfile.objects.get(custom_user=cls.premium_user)
        cls.premium_user_profile.user_type = UserProfile.UserType.PREMIUM
        cls.premium_user_profile.save()

        # Create a non-premium user
        cls.non_premium_user = CustomUser.objects.create_user(
            email="nonpremium@example.com",
            password="testpass123",
        )
        # Similarly, update the UserProfile for the non-premium user
        cls.non_premium_user_profile = UserProfile.objects.get(
            custom_user=cls.non_premium_user
        )
        cls.non_premium_user_profile.user_type = UserProfile.UserType.FREE
        cls.non_premium_user_profile.save()

        # Create a template
        cls.template = SavedUserTemplate.objects.create(
            author=cls.premium_user,
            name_of_template="Premium User's Template",
        )

        cls.client = Client()

    def test_detail_view_premium_user(self):
        # Login as premium user
        self.client.login(email="premium@example.com", password="testpass123")

        # Get the detail view
        response = self.client.get(
            reverse(
                "SavedUserTemplates:template-detail", kwargs={"pk": self.template.pk}
            )
        )

        # Check that the premium user can access their template's detail view
        self.assertEqual(response.status_code, 200)
        # print(response)
        # self.assertContains(response, self.template.name_of_template)

    def test_detail_view_non_premium_user(self):
        # Login as non-premium user
        self.client.login(email="nonpremium@example.com", password="testpass123")

        # Try to get the detail view of the premium user's template
        response = self.client.get(
            reverse(
                "SavedUserTemplates:template-detail", kwargs={"pk": self.template.pk}
            )
        )

        # Check that the non-premium user cannot access the detail view
        self.assertNotEqual(response.status_code, 200)

    def test_detail_view_not_logged_in(self):
        # Try to access the detail view without logging in
        response = self.client.get(
            reverse(
                "SavedUserTemplates:template-detail", kwargs={"pk": self.template.pk}
            )
        )

        # Check that anonymous users are redirected (usually to login page)
        self.assertEqual(response.status_code, 302)


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class TemplateUpdateViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create premium and non-premium users
        cls.premium_user = CustomUser.objects.create_user(
            email="premiumuser@example.com",
            password="premium_password",
        )
        cls.non_premium_user = CustomUser.objects.create_user(
            email="nonpremiumuser@example.com",
            password="nonpremium_password",
        )

        # The UserProfile for this user is automatically created by the post_save signal,
        # so we can retrieve it and update the user_type
        cls.premium_user_profile = UserProfile.objects.get(custom_user=cls.premium_user)
        cls.premium_user_profile.user_type = UserProfile.UserType.PREMIUM
        cls.premium_user_profile.save()

        # Similarly, update the UserProfile for the non-premium user
        cls.non_premium_user_profile = UserProfile.objects.get(
            custom_user=cls.non_premium_user
        )
        cls.non_premium_user_profile.user_type = UserProfile.UserType.FREE
        cls.non_premium_user_profile.save()

        # Create a template to be updated
        cls.template = SavedUserTemplate.objects.create(
            author=cls.premium_user,
            name_of_template="Initial Template Name",
            # ... other fields
        )

        cls.client = Client()

    def test_update_view_premium_user(self):
        self.client.login(email="premiumuser@example.com", password="premium_password")
        update_url = reverse(
            "SavedUserTemplates:update-template", kwargs={"pk": self.template.pk}
        )
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)

        # Now post updated data
        updated_data = {
            "name_of_template": "Updated Template Name",
            # ... other fields
        }
        response = self.client.post(update_url, updated_data)
        self.assertRedirects(response, reverse("SavedUserTemplates:list-templates"))

        # Verify the template was updated
        self.template.refresh_from_db()
        self.assertEqual(self.template.name_of_template, "Updated Template Name")

    def test_update_view_non_premium_user(self):
        self.client.login(
            email="nonpremiumuser@example.com", password="nonpremium_password"
        )
        update_url = reverse(
            "SavedUserTemplates:update-template", kwargs={"pk": self.template.pk}
        )
        response = self.client.get(update_url)
        self.assertNotEqual(response.status_code, 200)

    def test_update_view_not_logged_in(self):
        update_url = reverse(
            "SavedUserTemplates:update-template", kwargs={"pk": self.template.pk}
        )
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 302)  # Should redirect to login page


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class TemplateDeleteViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create premium and non-premium users
        cls.premium_user = CustomUser.objects.create_user(
            email="premiumuser@example.com",
            password="premium_password",
        )
        cls.non_premium_user = CustomUser.objects.create_user(
            email="nonpremiumuser@example.com",
            password="nonpremium_password",
        )

        # The UserProfile for this user is automatically created by the post_save signal,
        # so we can retrieve it and update the user_type
        cls.premium_user_profile = UserProfile.objects.get(custom_user=cls.premium_user)
        cls.premium_user_profile.user_type = UserProfile.UserType.PREMIUM
        cls.premium_user_profile.save()

        # Similarly, update the UserProfile for the non-premium user
        cls.non_premium_user_profile = UserProfile.objects.get(
            custom_user=cls.non_premium_user
        )
        cls.non_premium_user_profile.user_type = UserProfile.UserType.FREE
        cls.non_premium_user_profile.save()

        # Create a template to be deleted
        cls.template = SavedUserTemplate.objects.create(
            author=cls.premium_user,
            name_of_template="Template to be deleted",
            # ... other fields
        )

        cls.client = Client()

    def test_delete_view_premium_user(self):
        self.client.login(email="premiumuser@example.com", password="premium_password")
        delete_url = reverse(
            "SavedUserTemplate:delete-template", kwargs={"pk": self.template.pk}
        )
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)

        # Now post to delete
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse("SavedUserTemplate:list-templates"))

        # Verify the template was deleted
        with self.assertRaises(SavedUserTemplate.DoesNotExist):
            SavedUserTemplate.objects.get(pk=self.template.pk)

    def test_delete_view_non_premium_user(self):
        self.client.login(
            email="nonpremiumuser@example.com", password="nonpremium_password"
        )
        delete_url = reverse(
            "SavedUserTemplate:delete-template", kwargs={"pk": self.template.pk}
        )
        response = self.client.get(delete_url)
        self.assertNotEqual(response.status_code, 200)

    def test_delete_view_not_logged_in(self):
        delete_url = reverse(
            "SavedUserTemplate:delete-template", kwargs={"pk": self.template.pk}
        )
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 302)  # Should redirect to login page
