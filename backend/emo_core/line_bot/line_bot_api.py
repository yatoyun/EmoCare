from google.cloud import language_v1
from ..models import UserModel, TempRegister
from emo_core.models import EmotionData, ChatLogs, AdviceData
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from pathlib import Path
import uuid
import environ

# Environment and Configuration
BASE_DIR = Path(__file__).resolve().parent.parent

# import env file
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(Path(BASE_DIR, '.env'))
ACCESS_TOKEN = env('LINE_BOT_ACCESS_TOKEN')
CHANNEL_SECRET = env('LINE_BOT_CHANNEL_SECRET')
GOOGLE_APPLICATION_CREDENTIALS = env('GOOGLE_APPLICATION_CREDENTIALS')

# Initialize APIs
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

def generate_unique_token():
    return str(uuid.uuid4())

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']

        try:
            handler.handle(request.body.decode('utf-8'), signature)
        except (InvalidSignatureError, LineBotApiError):
            return HttpResponseForbidden()
        return HttpResponse()
    return HttpResponseBadRequest()

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_user_id = event.source.user_id
    text = event.message.text.lower()  # Normalize text

    if text == 'register':
        handle_registration(event, line_user_id)
    else:
        handle_chat(event, line_user_id, text)

# register functions
def handle_registration(event, line_user_id):
    user, created = UserModel.objects.get_or_create(line_user_id=line_user_id)
    if created:
        unique_token = generate_unique_token()
        TempRegister.objects.update_or_create(line_user_id=line_user_id, defaults={'token': unique_token})
        registration_url = f"http://localhost:3000?token={unique_token}"
        reply_text = f"Please register by visiting: {registration_url}"
    else:
        reply_text = "You are already registered."
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

# chat functions
def handle_chat(event, line_user_id, text):
    try:
        django_user = UserModel.objects.get(line_user_id=line_user_id)
    except UserModel.DoesNotExist:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="You are not registered."))
        return

    ChatLogs.objects.create(user=django_user, message=text)
    emotion_score, emotion_magnitude = analyze_emotion(text)
    EmotionData.objects.create(user=django_user, emotion_score=emotion_score, emotion_magnitude=emotion_magnitude)
    advice = generate_advice(emotion_score)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=advice))

def analyze_emotion(content):
    client = language_v1.LanguageServiceClient.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)
    document = language_v1.Document(content=content, type_=language_v1.Document.Type.PLAIN_TEXT, language='ja')
    response = client.analyze_sentiment(document=document)
    return response.document_sentiment.score, response.document_sentiment.magnitude

def generate_advice(emotion_score):
    # Implementation here
    return "This is a dummy advice."