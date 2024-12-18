from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class SavedUserTemplate(models.Model):
    # Custom_user model connected in 1 to many with SavedUserTemplates
    author = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    name_of_template = models.CharField(max_length=200, unique=True)
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

    def __str__(self) -> str:
        """Return a string representation of SavedUserTemplate"""
        return str(self.name_of_template)
