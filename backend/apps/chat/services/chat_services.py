from logging import getLogger
from openai import OpenAI
from django.conf import settings

from apps.chat.models import ChatMessage
from apps.user_statistics.services.user_statistics_services import get_recent_avg_statistics

logger = getLogger(__name__)

MAX_TOKENS = 200
SYSTEM_PROMPT = "あなたは相手の心を気遣うことが上手く、メンタルケアが得意です。相手のmessageとその感情分析値が渡されます。その感情分析値も考慮して返信してください。相手と同じ長さの返信をしてください。50文字以内で"

def get_gpt_response(user, prompt: str) -> str:
    """
    Connect to OpenAI API and get a response.
    """
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    emotion_score = get_recent_avg_statistics(user, prompt)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += get_before_messages(user)
    messages += [{"role": "user", "content": f"{prompt}:emotion_score={emotion_score}"}]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=MAX_TOKENS,
        n=1,
        temperature=0.7,
    )
    return response.choices[0].message.content

def save_chat_message(user, user_message: str, gpt_response: str) -> ChatMessage:
    """
    Save chat message to the database.
    """
    chat_message = ChatMessage.objects.create(
        user=user,
        user_message=user_message,
        gpt_response=gpt_response
    )
    return chat_message

def get_before_messages(user):
    """
    Get all chat messages from the database.
    """
    messages = ChatMessage.objects.filter(user=user)
    formatted_messages = []
    for message in messages:
        formatted_messages += [
            {"role": "user", "content": [{ "type": "text", "text": message.user_message }]},
            {"role": "assistant", "content": [{ "type": "text", "text": message.gpt_response }]}
        ]
    return formatted_messages

def get_chat_history(user, limit: int = -1) -> ChatMessage:
    """
    Get chat history for a user.
    """
    chat_history = ChatMessage.objects.filter(user=user).order_by('-created_at')
    if limit > 0:
        chat_history = chat_history[:limit]
    return chat_history
