from django.urls import reverse_lazy
from django.views import generic

from user_profile import mixins as user_mixins

from . import models

# Create your views here.


class CreateTemplateView(user_mixins.PremiumRequiredMixin, generic.CreateView):
    """View to create template."""

    model = models.SavedUserTemplate
    fields = [
        "name_of_template",
        "summary",
        "formal",
        "academic",
        "creative",
        "study_notes",
        "meeting_notes",
        "email_and_memo",
        "outline",
        "story_telling",
        "research_paper",
        "report",
        "resume",
    ]
    success_url = reverse_lazy("SavedUserTemplates:list-templates")
    extra_context = {"title_text": "Create Template", "button_text": "Create"}

    def form_valid(self, form):
        """Set the author of the current template to the user currently logged in."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class TemplateListView(user_mixins.PremiumRequiredMixin, generic.ListView):
    """Template list view."""

    model = models.SavedUserTemplate
    # queryset = models.SavedUserTemplate.objects

    def get_queryset(self):
        """Return the list of items for this view. Only list the templates that belong to the user currently logged in."""
        # Assuming 'author' is a ForeignKey to the User model
        return self.model.objects.filter(author=self.request.user)


class TemplateDetailView(user_mixins.PremiumRequiredMixin, generic.DetailView):
    """Detail view of SavedUserTemplates."""

    model = models.SavedUserTemplate


class TemplateUpdateView(user_mixins.PremiumRequiredMixin, generic.UpdateView):
    """View to update template."""

    model = models.SavedUserTemplate
    fields = [
        "name_of_template",
        "summary",
        "formal",
        "academic",
        "creative",
        "study_notes",
        "meeting_notes",
        "email_and_memo",
        "outline",
        "story_telling",
        "research_paper",
        "report",
        "resume",
    ]
    success_url = reverse_lazy("SavedUserTemplates:list-templates")
    extra_context = {"title_text": "Edit Template", "button_text": "Save"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["template"] = self.object if self.object else None
        return context


class TemplateDeleteView(user_mixins.PremiumRequiredMixin, generic.DeleteView):
    """View to delete template."""

    # Note to self:
    #

    model = models.SavedUserTemplate
    success_url = reverse_lazy("SavedUserTemplate:list-templates")
    template_name = "SavedUserTemplates/savedusertemplate_delete.html"
    extra_context = {"title_text": "Delete Template"}
