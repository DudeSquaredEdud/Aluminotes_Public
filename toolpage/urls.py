from django.urls import path
from toolpage import views as toolpage_views

app_name = "toolpage"

urlpatterns = [
    path(
        "toolpage_app/", toolpage_views.ToolpageAppView.as_view(), name="toolpage_app"
    ),
    path(
        "toolpage_update/",
        toolpage_views.ToolpageTemplateUpdate.as_view(),
        name="toolpage_template_update",
    ),
    path(
        "reshape/",
        toolpage_views.ReshapeText,
        name="toolpage_reshape",
    ),
    path(
        "readfile/",
        toolpage_views.readfile,
        name="toolpage_readfile",
    ),
    path(
        "transcribe_audio/",
        toolpage_views.transcribe_audio,
        name="toolpage_transcribe_audio",
    ),
]
