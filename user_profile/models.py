"""User profile app models."""

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from users.models import CustomUser


class UserProfile(models.Model):
    """UserProfile model class."""

    class Gender(models.IntegerChoices):
        """Gender choice class."""

        NONE = 0
        FEMALE = 1
        MALE = 2
        OTHER = 3

    class UserType(models.IntegerChoices):
        """User Type Choice"""

        FREE = 0
        PREMIUM = 1

    custom_user = models.OneToOneField("users.CustomUser", on_delete=models.CASCADE)
    gender = models.IntegerField(choices=Gender.choices, default=Gender.NONE)
    age = models.IntegerField(default=21)
    picture = models.ImageField(upload_to="profile_pictures/", blank=True)
    user_type = models.IntegerField(choices=UserType.choices, default=UserType.FREE)
    phone = models.CharField(max_length=20, blank=True)
    last_prompt_time = models.DateTimeField(default=timezone.now)
    last_file_upload_time = models.DateTimeField(default=timezone.now)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        """Return a string representation of SavedUserTemplate"""
        return str(self.custom_user)


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    """Create an object of UserProfile when a user CustomUser object is created."""
    if sender and created:
        UserProfile.objects.create(custom_user=instance)


post_save.connect(create_profile, sender=CustomUser)
