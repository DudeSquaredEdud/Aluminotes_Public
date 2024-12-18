from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import UserProfile
from django.urls import reverse
from user_profile import views
from django.test import TestCase, override_settings


# Create your tests here.


class UserProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = get_user_model().objects.create_user(
            email="email", password="password"
        )

    def test_user_profile_creation(self):
        # Check if UserProfile is created when a user is created
        user_profile = UserProfile.objects.get(custom_user=self.user)
        self.assertEqual(user_profile.gender, UserProfile.Gender.NONE)
        self.assertEqual(user_profile.age, 21)
        self.assertEqual(user_profile.user_type, UserProfile.UserType.FREE)

    def test_user_profile_str_representation(self):
        # Check if __str__ method returns the correct string representation
        user_profile = UserProfile.objects.get(custom_user=self.user)
        self.assertEqual(str(user_profile), str(self.user))


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class UserProfileDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = get_user_model().objects.create_user(
            email="email", password="password"
        )
        # Create a test user profile
        cls.user_profile = UserProfile.objects.get(custom_user=cls.user)

    def test_detail_view_access(self):
        client = Client()
        client.login(email="email", password="password")
        response = client.get(reverse("user_profile:profile_detail"))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_content(self):
        client = Client()
        client.login(email="email", password="password")
        response = client.get(reverse("user_profile:profile_detail"))
        self.assertContains(response, "User Profile")


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class UserProfileUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = get_user_model().objects.create_user(
            email="email", password="password"
        )
        # Create a test user profile
        cls.user_profile = UserProfile.objects.get(custom_user=cls.user)

    def test_update_view_access(self):
        client = Client()
        client.login(email="email", password="password")
        response = client.get(reverse("user_profile:profile_update"))
        self.assertEqual(response.status_code, 200)

    def test_update_view_content(self):
        client = Client()
        client.login(email="email", password="password")
        response = client.get(reverse("user_profile:profile_update"))
        self.assertContains(response, "Update Profile")


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class UserProfileDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = get_user_model().objects.create_user(
            email="email", password="password"
        )
        # Create a test user profile
        cls.user_profile = UserProfile.objects.get(custom_user=cls.user)

    def test_delete_view_access(self):
        client = Client()
        client.login(email="email", password="password")
        response = client.get(
            reverse("user_profile:profile_delete", kwargs={"pk": self.user_profile.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Are you sure you want to delete ")

    def test_delete_view_deletes_profile(self):
        client = Client()
        client.login(email="email", password="password")
        response = client.post(
            reverse("user_profile:profile_delete", kwargs={"pk": self.user_profile.pk})
        )
        self.assertEqual(
            response.status_code, 302
        )  # Redirects after successful deletion
        self.assertFalse(
            UserProfile.objects.filter(pk=self.user_profile.pk).exists()
        )  # Check if profile is deleted
