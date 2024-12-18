from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from toolpage.models import ToolpageTemplate
from django.test import TestCase, override_settings


User = get_user_model()


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class ToolpageTemplateModelTest(TestCase):

    @classmethod
    def setUpTestData(self):
        # Create a user and automatically create a ToolpageTemplate via signal
        User = get_user_model()
        self.user = User.objects.create_user(
            email="testuser@example.com",  # Use the email as the primary identifier if that's what your model uses
            password="testpass",
            # Include any other required fields according to your CustomUser model
        )

        self.toolpage_template, created = ToolpageTemplate.objects.get_or_create(
            user=self.user,
            defaults={
                "summary": True,
                "formal": False,
                # Initialize other fields as needed
            },
        )

    def test_toolpage_template_creation(self):
        # Test that the ToolpageTemplate instance has been created successfully.
        self.assertIsInstance(self.toolpage_template, ToolpageTemplate)
        self.assertEqual(self.toolpage_template.user, self.user)

    def test_default_boolean_fields(self):
        # Test that the default values of boolean fields are False
        self.assertFalse(self.toolpage_template.summary)
        self.assertFalse(self.toolpage_template.formal)
        self.assertFalse(self.toolpage_template.academic)
        self.assertFalse(self.toolpage_template.creative)
        self.assertFalse(self.toolpage_template.study_notes)
        self.assertFalse(self.toolpage_template.meeting_notes)
        self.assertFalse(self.toolpage_template.email_and_memo)
        self.assertFalse(self.toolpage_template.outline)
        self.assertFalse(self.toolpage_template.story_telling)
        self.assertFalse(self.toolpage_template.research_paper)
        self.assertFalse(self.toolpage_template.report)
        self.assertFalse(self.toolpage_template.resume)

    def test_toolpage_template_str(self):
        # Test the string representation of the ToolpageTemplate instance.
        self.assertEqual(str(self.toolpage_template), str(self.user))


from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import ToolpageTemplate
from SavedUserTemplates.models import SavedUserTemplate

# Create your tests here.


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class ToolpageAppViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = get_user_model().objects.create_user(
            email="email", password="password"
        )
        # Create a test toolpage template for the user
        if not ToolpageTemplate.objects.filter(user=cls.user).exists():
            cls.toolpage_template = ToolpageTemplate.objects.create(
                user=cls.user,
                summary=False,
                formal=False,
                academic=False,
                creative=False,
                study_notes=False,
                meeting_notes=False,
                email_and_memo=False,
                outline=False,
                story_telling=False,
                research_paper=False,
                report=False,
                resume=False,
            )

    def test_toolpage_app_view(self):
        client = Client()
        client.login(email="email", password="password")
        response = client.get(reverse("toolpage:toolpage_app"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Summarize")
