from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class ToolpageTemplate(models.Model):
    # User Profile
    user = models.OneToOneField(
        "users.CustomUser", on_delete=models.CASCADE, null=True, blank=True
    )
    # Voices
    summary = models.BooleanField(default=False)
    formal = models.BooleanField(default=False)
    academic = models.BooleanField(default=False)
    creative = models.BooleanField(default=False)
    study_notes = models.BooleanField(default=False)
    meeting_notes = models.BooleanField(default=False)
    email_and_memo = models.BooleanField(default=False)
    outline = models.BooleanField(default=False)
    story_telling = models.BooleanField(default=False)
    research_paper = models.BooleanField(default=False)
    report = models.BooleanField(default=False)
    resume = models.BooleanField(default=False)
    bionic_reading = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.user)


# Automatically make a saved template when a user makes an account
@receiver(post_save, sender="users.CustomUser")
def create_toolpage_template(sender, instance, created, **kwargs):
    """Used to automatically create a toolpage template."""
    if sender and created:
        ToolpageTemplate.objects.create(user=instance)


# Automation for connecting a toolpage template to the userprofile it belongs to
post_save.connect(create_toolpage_template, sender="users.CustomUser")
