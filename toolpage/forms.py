from django import forms
from .models import ToolpageTemplate
from SavedUserTemplates.models import SavedUserTemplate


class ToolpageTemplateForm(forms.ModelForm):
    class Meta:
        model = ToolpageTemplate
        exclude = ["user"]


class ToolpageSavedUserTemplateForm(forms.Form):
    class Meta:
        model = SavedUserTemplate
        exclude = [""]
