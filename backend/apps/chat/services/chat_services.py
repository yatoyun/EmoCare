from logging import getLogger
from openai import OpenAI
# from openai.error import OpenAIError  # 必要に応じて追加

from apps.chat.models import ChatMessage
from apps.user_statistics.services.user_statistics_services import get_recent_avg_statistics
from apps.common.utils import get_secret_value

logger = getLogger(__name__)

MAX_TOKENS = 200
SYSTEM_PROMPT = "あなたは相手の心を気遣うことが上手く、メンタルケアが得意です。相手のmessageとその感情分析値が渡されます。その感情分析値も考慮して返信してください。相手と同じ長さの返信をしてください。50文字以内で"

def get_gpt_response(user, prompt: str) -> str:
    """
    OpenAI APIを使用してGPTからの応答を取得します。

    Args:
        user: ユーザーオブジェクト
        prompt (str): ユーザーからの入力メッセージ

    Returns:
        str: GPTからの応答テキスト

    Raises:
        ValueError: API keyが取得できない場合
        OpenAIError: OpenAI APIからエラーが返された場合
    """
    try:
        OPENAI_API_KEY = get_secret_value("OPENAI_API")
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key not found")

        client = OpenAI(api_key=OPENAI_API_KEY)
        emotion_score = get_recent_avg_statistics(user, prompt)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(get_before_messages(user))
        messages.append({"role": "user", "content": f"{prompt}:emotion_score={emotion_score}"})

        logger.info(f"Sending request to GPT for user {user.user_id}")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=MAX_TOKENS,
            n=1,
            temperature=0.7,
        )
        return response.choices[0].message.content

    except ValueError as e:
        logger.error(f"Configuration error: {repr(e)}")
        raise
    except Exception as e:
        logger.error(f"OpenAI API error for user {user.user_id}: {repr(e)}")
        raise

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
    ユーザーの過去のチャット履歴を取得してOpenAI APIのメッセージ形式に変換します。

    Args:
        user: ユーザーオブジェクト

    Returns:
        list: フォーマット済みのメッセージリスト
    """
    messages = ChatMessage.objects.filter(user=user)
    formatted_messages = []
    for message in messages:
        formatted_messages.extend([
            {"role": "user", "content": message.user_message},
            {"role": "assistant", "content": message.gpt_response}
        ])
    return formatted_messages

def get_chat_history(user, limit: int = -1) -> ChatMessage:
    """
    Get chat history for a user.
    """
    chat_history = ChatMessage.objects.filter(user=user).order_by('-created_at')
    if limit > 0:
        chat_history = chat_history[:limit]
    return chat_history
