from django.urls import path

from SavedUserTemplates import views

app_name = "SavedUserTemplates"
urlpatterns = [
    path(
        "templates/create", views.CreateTemplateView.as_view(), name="create-template"
    ),  # Create
    path(
        "templates/", views.TemplateListView.as_view(), name="list-templates"
    ),  # Read, list
    path(
        "templates/<int:pk>/detail",
        views.TemplateDetailView.as_view(),
        name="template-detail",
    ),  # Read, detail
    path(
        "templates/<int:pk>/update",
        views.TemplateUpdateView.as_view(),
        name="update-template",
    ),  # Update
    path(
        "templates/<int:pk>/delete",
        views.TemplateDeleteView.as_view(),
        name="delete-template",
    ),
]
