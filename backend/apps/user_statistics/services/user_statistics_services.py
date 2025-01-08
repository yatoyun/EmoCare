from google.cloud import language_v2
from django.conf import settings
from django.db.models import Avg, Count, Q
from django.db.models.functions import TruncDay, TruncWeek
from scipy import stats

from apps.user_statistics.models import Statistics
from apps.chat.models import ChatMessage
from apps.users.models import User

AVG_MESSAGES_LIMIT = 5

def get_user_statistics(user: User, limit: int = -1) -> Statistics:
    """
    Get Statistics on a per-user basis.
    """
    user_statistics = Statistics.objects.filter(user=user).order_by('-created_at')[:limit]
    if limit > 0:
        user_statistics = user_statistics[:limit]
    return user_statistics

def get_recent_avg_statistics(user: User, text: str) -> Statistics:
    """
    Get the average statistics for a user.
    """
    recent_statistics_scores = get_user_statistics(user, AVG_MESSAGES_LIMIT)
    new_emotion_score = get_new_emotion_score(text)
    save_new_statistics(user, new_emotion_score[0], new_emotion_score[1])

    avg_score = 0
    for emotion in recent_statistics_scores:
        avg_score += emotion.emotion_score

    avg_score += new_emotion_score[0]
    if len(recent_statistics_scores) > 0:
        avg_score /= len(recent_statistics_scores) + 1
    return round(avg_score, 2)

def get_new_emotion_score(content: str) -> tuple:
    """
    Get the new emotion score for a user.
    """
    client = language_v2.LanguageServiceClient.from_service_account_json(settings.GOOGLE_APPLICATION_CREDENTIALS)
    document = language_v2.Document(content=content, type_=language_v2.Document.Type.PLAIN_TEXT, language_code='ja')
    encoding_type = language_v2.EncodingType.UTF8
    response = client.analyze_sentiment(request={"document": document, "encoding_type": encoding_type})
    return response.document_sentiment.score, response.document_sentiment.magnitude

def save_new_statistics(user: User, emotion_score: float, emotion_magnitude: float) -> Statistics:
    """
    Save new statistics to the database.
    """
    statistics = Statistics.objects.create(
        user=user,
        emotion_score=emotion_score,
        emotion_magnitude=emotion_magnitude
    )
    return statistics

def gather_user_statistics(user):
    """
    Get user statistics list.
    """

    # user's emotion score and emotion magnitude
    emotion_data_qs = Statistics.objects.filter(user=user)
    emotion_scores = list(emotion_data_qs.values_list("emotion_score", flat=True))
    emotion_magnitudes = list(emotion_data_qs.values_list("emotion_magnitude", flat=True))

    # avg score and count per day
    daily_emotion_stats = (
        emotion_data_qs
        .annotate(date=TruncDay("created_at"))
        .values("date")
        .annotate(avg_score=Avg("emotion_score"), count=Count("id"))
        .order_by("date")
    )

    # avg score and count per week
    weekly_emotion_stats = (
        emotion_data_qs
        .annotate(week=TruncWeek("created_at"))
        .values("week")
        .annotate(avg_score=Avg("emotion_score"), count=Count("id"))
        .order_by("week")
    )

    # summary of ChatMessage per day
    daily_chat_stats = (
        ChatMessage.objects
        .annotate(date=TruncDay("created_at"))
        .values("date")
        .annotate(total_messages=Count("id"))
        .order_by("date")
    )

    # summary of ChatMessage per week
    weekly_chat_stats = (
        ChatMessage.objects
        .annotate(week=TruncWeek("created_at"))
        .values("week")
        .annotate(total_messages=Count("id"))
        .order_by("week")
    )

    # classification of sentiment per day
    daily_sentiment_classification = (
        emotion_data_qs
        .annotate(date=TruncDay("created_at"))
        .values("date")
        .annotate(
            positive=Count("id", filter=Q(emotion_score__gt=0.25)),
            negative=Count("id", filter=Q(emotion_score__lt=-0.25)),
            neutral=Count("id", filter=Q(emotion_score__gte=-0.15, emotion_score__lte=0.15)),
            mixed=Count(
                "id",
                filter=Q(
                    emotion_score__gt=-0.15,
                    emotion_score__lt=0.15,
                    emotion_magnitude__gt=0.5
                )
            ),
        )
        .order_by("date")
    )

    # classification of sentiment per week
    weekly_sentiment_classification = (
        emotion_data_qs
        .annotate(week=TruncWeek("created_at"))
        .values("week")
        .annotate(
            positive=Count("id", filter=Q(emotion_score__gt=0.25)),
            negative=Count("id", filter=Q(emotion_score__lt=-0.25)),
            neutral=Count("id", filter=Q(emotion_score__gte=-0.15, emotion_score__lte=0.15)),
            mixed=Count(
                "id",
                filter=Q(
                    emotion_score__gt=-0.15,
                    emotion_score__lt=0.15,
                    emotion_magnitude__gt=0.5
                )
            ),
        )
        .order_by("week")
    )

    # scatter_data
    scatter_data = list(zip(emotion_scores, emotion_magnitudes))

    # Correlation, Skewness, Kurtosis
    # Initialize with None to indicate undefined values
    correlation_score_magnitude = None
    skewness_value = None
    kurtosis_value = None
    descriptive_skewness = "undefined"
    descriptive_kurtosis = "undefined"

    if len(emotion_scores) > 1:
        # Check if all emotion_scores are identical
        if len(set(emotion_scores)) > 1:
            try:
                corr, _ = stats.pearsonr(emotion_scores, emotion_magnitudes)
                correlation_score_magnitude = corr if not math.isnan(corr) else None
            except Exception as e:
                correlation_score_magnitude = None

            try:
                skew = stats.skew(emotion_scores)
                skewness_value = skew if not math.isnan(skew) else None
            except Exception as e:
                skewness_value = None

            try:
                kurt = stats.kurtosis(emotion_scores)
                kurtosis_value = kurt if not math.isnan(kurt) else None
            except Exception as e:
                kurtosis_value = None
        else:
            # Data is constant; correlation, skewness, and kurtosis are undefined
            correlation_score_magnitude = None
            skewness_value = None
            kurtosis_value = None

    # Describe skewness
    if skewness_value is not None:
        if skewness_value > 0:
            descriptive_skewness = "positive"
        elif skewness_value < 0:
            descriptive_skewness = "negative"
        else:
            descriptive_skewness = "neutral"
    else:
        descriptive_skewness = "undefined"

    # Describe kurtosis
    if kurtosis_value is not None:
        descriptive_kurtosis = "less reliable" if kurtosis_value > 3 else "reliable"
    else:
        descriptive_kurtosis = "undefined"

    # Final response
    stats_response = {
        "daily_emotion_stats": list(daily_emotion_stats),
        "weekly_emotion_stats": list(weekly_emotion_stats),
        "daily_chat_stats": list(daily_chat_stats),
        "weekly_chat_stats": list(weekly_chat_stats),
        "daily_sentiment_classification": list(daily_sentiment_classification),
        "weekly_sentiment_classification": list(weekly_sentiment_classification),
        "scatter_data": scatter_data,
        "correlation_score_magnitude": correlation_score_magnitude,
        "skewness": {
            "value": skewness_value,
            "description": descriptive_skewness
        },
        "kurtosis": {
            "value": kurtosis_value,
            "description": descriptive_kurtosis
        },
    }

    return stats_response
