from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Custom_User_Settings(models.Model):
    # Settings model connected in 1 to 0..1 with user_profile

    user_settings = models.OneToOneField(
        "users.CustomUser", on_delete=models.CASCADE, null=True, blank=True
    )
    dark_mode = models.BooleanField(default=False)
    retain_last_used_options = models.BooleanField(default=False)
    theme = models.CharField(max_length=20, default="galactic_blood")

    # Show the owner of the settings in admin
    def __str__(self) -> str:
        return str(self.user_settings)


# Automatically make a saved template when a user makes an account
@receiver(post_save, sender="users.CustomUser")
def create_settings(sender, instance, created, **kwargs):
    """Used to automatically create a toolpage template."""
    if sender and created:
        Custom_User_Settings.objects.create(user_settings=instance)


# Automation for connecting a toolpage template to the userprofile it belongs to
post_save.connect(create_settings, sender="users.CustomUser")
