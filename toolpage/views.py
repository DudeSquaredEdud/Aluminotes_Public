import json
import os.path
import os
import re
import tempfile
from datetime import timedelta
from html import escape as html_escape

from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

# GenAI
import google.generativeai as genai
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


# for file conversion
import pypandoc
from pypdf import PdfReader

# Speech Recognition
import speech_recognition as sr
from pydub import AudioSegment

from Custom_User_Settings.models import Custom_User_Settings
from SavedUserTemplates.models import SavedUserTemplate
from user_profile import mixins as user_mixins

from .forms import ToolpageTemplateForm
from .models import ToolpageTemplate


SCOPES = ["https://www.googleapis.com/auth/generative-language.retriever"]


def load_creds():
    """Converts `client_secret.json` to a credential object.

    This function caches the generated tokens to minimize the use of the
    consent screen.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(e)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "toolpage/client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


class ToolpageAppView(user_mixins.UserProfileRequiredMixin, View):
    template_name = "toolpage/toolpage_app.html"

    def get(self, request, *args, **kwargs):
        current_user_template = ToolpageTemplate.objects.filter(
            user=request.user
        ).first()
        toolpage_template_form: ToolpageTemplateForm = None

        user_settings, created = Custom_User_Settings.objects.get_or_create(
            user_settings=request.user
        )

        if user_settings.retain_last_used_options:
            toolpage_template_form = ToolpageTemplateForm(
                initial={
                    "summary": current_user_template.summary,
                    "formal": current_user_template.formal,
                    "academic": current_user_template.academic,
                    "creative": current_user_template.creative,
                    "study_notes": current_user_template.study_notes,
                    "meeting_notes": current_user_template.meeting_notes,
                    "email_and_memo": current_user_template.email_and_memo,
                    "outline": current_user_template.outline,
                    "story_telling": current_user_template.story_telling,
                    "research_paper": current_user_template.research_paper,
                    "report": current_user_template.report,
                    "resume": current_user_template.resume,
                    "bionic_reading": current_user_template.bionic_reading,
                }
            )
        else:
            toolpage_template_form = ToolpageTemplateForm(
                initial={
                    "summary": False,
                    "formal": False,
                    "academic": False,
                    "creative": False,
                    "study_notes": False,
                    "meeting_notes": False,
                    "email_and_memo": False,
                    "outline": False,
                    "story_telling": False,
                    "research_paper": False,
                    "report": False,
                    "resume": False,
                    "bionic_reading": False,
                }
            )

        rendered_toolpage_template_form = toolpage_template_form.render(
            "toolpage/form_current_template.html"
        )

        saved_user_template = SavedUserTemplate.objects.filter(author=request.user)
        rendered_saved_user_template_form = render(
            request,
            "toolpage/form_saved_template.html",
            {"user_templates": saved_user_template},
        ).content.decode("utf-8")

        context = {
            "toolpage_template_form": rendered_toolpage_template_form,
            "saved_user_template_loader": rendered_saved_user_template_form,
        }

        return render(request, self.template_name, context)


class ToolpageTemplateUpdate(View):

    def post(self, request, *args, **kwargs):
        form = ToolpageTemplateForm(request.POST)
        if form.is_valid():
            user_object = ToolpageTemplate.objects.filter(user=request.user).first()
            form = ToolpageTemplateForm(instance=user_object, data=request.POST)
            form.save()
            data = {"message": "Form saved successfully!"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return HttpResponse(
                json.dumps({"message": "Form is not valid"}),
                content_type="application/json",
            )


def generate_error(error_type: str):
    error_messages = {
        "no_options": "ERR: Please select at least one option.",
        "short": "ERR: Please try again with a longer text. Minimum length is 10 words.",
        "length_no_acct": "ERR: Text length is too long. Sign up or log in to increase the limit.",
        "length_free": "ERR: Text length is too long. Please try again with a shorter text, or upgrade to Aluminotes Premium.",
        "length_premium": "ERR: Text length is too long. Please try again with a shorter text.",
        "query_limit": "ERR: Query limit reached. Please try again later.",
        "query_limit_no_acct": "ERR: Query limit reached. Sign up or log in to increase the limit.",
        "vulgar": "ERR: Please remove any vulgar language.",
        "unknown": "ERR: An unknown error occurred.",
    }
    print(error_messages[error_type])
    yield json.dumps(error_messages[error_type])


def ReshapeText(request):
    try:
        if request.method != "POST":
            return JsonResponse({"error": "Invalid request method"}, status=400)
        data = json.loads(request.body)
        prompt = html_escape(data.get("prompt"))
        bionic_reading_check = data.get("bionic_reading_check")
        profile = request.user.userprofile

        prompt_length = len(prompt.split(" "))

        # Error Checking
        print("error checking")
        if prompt[0] == ":" and not bionic_reading_check:
            return StreamingHttpResponse(
                generate_error("no_options"), content_type="text/event-stream"
            )
        if prompt_length < 10:
            return StreamingHttpResponse(
                generate_error("short"), content_type="text/event-stream"
            )

        if profile.user_type == 2:  # No account. CHANGE AS NEEDED
            if prompt_length > 250:
                return StreamingHttpResponse(
                    generate_error("length_no_acct"), content_type="text/event-stream"
                )
            if (timezone.now() - profile.last_prompt_time) < timedelta(seconds=30):
                return StreamingHttpResponse(
                    generate_error("query_limit_no_acct"),
                    content_type="text/event-stream",
                )

        if profile.user_type == 0:  # Free user
            if prompt_length > 500:
                return StreamingHttpResponse(
                    generate_error("length_free"), content_type="text/event-stream"
                )
            if (timezone.now() - profile.last_prompt_time) < timedelta(seconds=12):
                return StreamingHttpResponse(
                    generate_error("query_limit"), content_type="text/event-stream"
                )

        elif profile.user_type == 1:  # Premium user
            if prompt_length > 8000:
                return StreamingHttpResponse(
                    generate_error("length_premium"), content_type="text/event-stream"
                )
            if (timezone.now() - profile.last_prompt_time) < timedelta(seconds=6):
                return StreamingHttpResponse(
                    generate_error("query_limit"), content_type="text/event-stream"
                )

        profile.last_prompt_time = timezone.now()
        profile.save()

        # if no errors, continue as normal
        creds = load_creds()
        genai.configure(credentials=creds)
        # It blocks too much stuff apparently
        unsafe_settings = [
            {
                "category": "HARM_CATEGORY_DANGEROUS",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]
        model = genai.GenerativeModel("REDACTED")

        result = model.generate_content(
            prompt, stream=True, safety_settings=unsafe_settings
        )

        def generate_response():
            try:
                for chunk in result:
                    yield json.dumps(chunk.text) + "\n"
            except Exception as chunk_error:
                # No clue why I can't do this one like the rest...
                if "Invalid operation" in str(chunk_error):
                    yield json.dumps("\nPlease remove any vulgar language.")
                else:
                    yield json.dumps("An unknown error occurred.")

        return StreamingHttpResponse(
            generate_response(), content_type="text/event-stream"
        )

    except Exception as reshape_error:
        print("reshape error")
        print(reshape_error)
        return StreamingHttpResponse(
            generate_error("unknown"), content_type="text/event-stream"
        )


def readfile(request):
    profile = request.user.userprofile
    # Error handling
    try:
        if request.method != "POST":
            return JsonResponse({"error": "Invalid request method"}, status=400)

        if not request.FILES:
            return JsonResponse({"error": "No file provided"}, status=400)

        # a 5 sec delay between uploads
        if (timezone.now() - profile.last_file_upload_time) < timedelta(seconds=5):
            return JsonResponse(
                {"error": "Please wait 5 seconds between uploads"}, status=400
            )
        else:
            profile.last_file_upload_time = timezone.now()
            profile.save()

        # get the file from the request
        file = request.FILES.get("file")
        # check file size
        if file.size > 5 * 1024 * 1024:  # 5 MB limit
            return JsonResponse({"error": "File size exceeds 5 MB limit"}, status=400)

        file_type = file.name.split(".")[-1]  # file type
        temp_file = tempfile.NamedTemporaryFile(suffix="." + file_type, delete=True)
        # chunking uploads work better than single-chunk uploads
        # length limits
        if profile.user_type == 0:
            max_text_length = 500
        elif profile.user_type == 1:
            max_text_length = 8000

        for chunk in file.chunks():
            temp_file.write(chunk)

        # if it's not a pdf, we use pypandoc
        if file_type != "pdf":
            try:
                # convert and close
                text = pypandoc.convert_file(temp_file.name, "plain")
                text_length = len(text.split(" "))
                if text_length > max_text_length:
                    temp_file.close()
                    return JsonResponse({"error": "File Text Too Long"}, status=400)
                temp_file.close()
                return HttpResponse(text)
            except Exception as conversion_error:
                print(f"Error converting file: {conversion_error}")
                temp_file.close()
                return JsonResponse({"error": "Failed to convert file"}, status=400)
        # Otherwise, we use pdfreader
        try:
            pdf_reader = PdfReader(temp_file.name)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text(extraction_mode="layout")
                print(page_text)
                text += page_text
                text_length = len(text.split(" ")) - 1
                if text_length > max_text_length:
                    temp_file.close()
                    return JsonResponse({"error": "File Text Too Long"}, status=400)
            text = re.sub("[ ]{2,}", " ", text)
            temp_file.close()
            return HttpResponse(text)
        except Exception as pdf_conversion_error:
            print(f"Error reading PDF: {pdf_conversion_error}")
            temp_file.close()
            return JsonResponse({"error": "Failed to read PDF"}, status=400)

    except Exception as file_error:
        print("File Error")
        print(file_error)
        return JsonResponse({"error": "File unable to be converted"}, status=400)


@csrf_exempt
def transcribe_audio(request):
    if request.method == "POST":
        try:
            audio_file = request.FILES.get("audio")
            if not audio_file:
                return JsonResponse({"error": "No audio file received"}, status=400)

            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".webm"
            ) as temp_audio:
                for chunk in audio_file.chunks():
                    temp_audio.write(chunk)
                temp_audio_path = temp_audio.name

            # Convert webm to wav
            audio = AudioSegment.from_file(temp_audio_path, format="webm")
            wav_path = temp_audio_path.replace(".webm", ".wav")
            audio.export(wav_path, format="wav")

            # Perform transcription
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)

            # Clean up temporary files
            os.remove(temp_audio_path)
            os.remove(wav_path)

            return JsonResponse({"transcription": text})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
