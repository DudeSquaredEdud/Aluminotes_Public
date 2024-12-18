from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .models import Custom_User_Settings
from .views import CreateSettingsView
from django.test import TestCase, override_settings


# Create your tests here.

User = get_user_model()


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class CustomUserSettingsModelTest(TestCase):
    def setUp(self):
        # Create a CustomUser instance to trigger the signal
        self.user = User.objects.create_user(
            email="testuser@email.com", password="testpass123"
        )

        # Setup the URL using reverse
        self.url = reverse("Custom_User_Settings:list-settings")

        # Setup request factory
        self.factory = RequestFactory()

    def test_custom_user_settings_creation(self):
        # Check that Custom_User_Settings instance has been created
        user_settings = Custom_User_Settings.objects.get(user_settings=self.user)
        self.assertIsNotNone(user_settings)
        self.assertEqual(user_settings.user_settings, self.user)

    def test_default_values(self):
        # Verify default values of created Custom_User_Settings
        user_settings = Custom_User_Settings.objects.get(user_settings=self.user)
        self.assertFalse(user_settings.dark_mode)

    def test_str_representation(self):
        # Test the __str__ method of Custom_User_Settings
        user_settings = Custom_User_Settings.objects.get(user_settings=self.user)
        self.assertEqual(str(user_settings), str(self.user))

    def test_get_create_settings_view(self):
        # Create an instance of a GET request.
        request = self.factory.get(reverse("Custom_User_Settings:list-settings"))
        request.user = self.user  # simulate logged-in user

        # Use this request to get the response from the view
        response = CreateSettingsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        # Check that the response contains the words "user settings"
        self.assertIn("user settings", response.content.decode("utf-8").lower())

    def test_post_create_settings_view(self):
        # Perform a POST request with darkMode as 'on'
        response = self.client.post(self.url, {"darkMode": "on"})

        # Check that the response is 200
        self.assertEqual(response.status_code, 200)

        # Fetch the updated settings from the database
        user_settings = Custom_User_Settings.objects.get(user_settings=self.user)
        self.assertTrue(user_settings.dark_mode)  # Verify dark mode is enabled

        # Perform a POST request with darkMode as not 'on' (unchecked)
        response = self.client.post(
            self.url,
            {
                "darkMode": "off",  # Assuming unchecked sends 'off' or no key-value at all
            },
        )

        # Fetch the updated settings from the database
        user_settings = Custom_User_Settings.objects.get(user_settings=self.user)
        self.assertFalse(user_settings.dark_mode)  # Verify dark mode is disabled
