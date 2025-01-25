import math
from typing import List, Dict, Any, Optional, Tuple
import logging
from google.cloud import language_v2
from django.conf import settings
from django.db.models import Avg, Count, Q
from django.db.models.functions import TruncDay, TruncWeek
from scipy import stats

from apps.user_statistics.models import Statistics
from apps.chat.models import ChatMessage
from apps.users.models import User
from apps.common.utils import get_secret_value

logger = logging.getLogger(__name__)

# Constants
AVG_MESSAGES_LIMIT = 5
SENTIMENT_THRESHOLDS = {
    'POSITIVE': 0.25,
    'NEGATIVE': -0.25,
    'NEUTRAL_MIN': -0.15,
    'NEUTRAL_MAX': 0.15,
    'MIXED_MAGNITUDE': 0.5
}

def get_user_statistics(user: User, limit: int = -1) -> List[Statistics]:
    """
    Get Statistics on a per-user basis.
    
    Args:
        user (User): User object
        limit (int): Number of records to return (-1 for all)
    
    Returns:
        List[Statistics]: List of statistics objects
    """
    query = Statistics.objects.filter(user=user).order_by('-created_at')
    return query[:limit] if limit > 0 else query

def get_recent_avg_statistics(user: User, text: str) -> float:
    """
    Get the average statistics for a user.
    
    Args:
        user (User): User object
        text (str): Text to analyze
        
    Returns:
        float: Average emotion score
    """
    try:
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
    except Exception as e:
        logger.error(f"Error calculating recent average statistics: {e}")
        raise

def get_new_emotion_score(content: str) -> Tuple[float, float]:
    """
    Get the new emotion score for a user.
    
    Args:
        content (str): Text content to analyze
        
    Returns:
        Tuple[float, float]: Tuple of (emotion_score, emotion_magnitude)
        
    Raises:
        GoogleAPIError: When API call fails
    """
    try:
        GOOGLE_APPLICATION_CREDENTIALS = get_secret_value("GOOGLE_APPLICATION_CREDENTIALS")
        client = language_v2.LanguageServiceClient.from_service_account_info(GOOGLE_APPLICATION_CREDENTIALS)
        document = language_v2.Document(
            content=content,
            type_=language_v2.Document.Type.PLAIN_TEXT,
            language_code='ja'
        )
        encoding_type = language_v2.EncodingType.UTF8
        response = client.analyze_sentiment(
            request={"document": document, "encoding_type": encoding_type}
        )
        return response.document_sentiment.score, response.document_sentiment.magnitude
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}")
        raise

def save_new_statistics(user: User, emotion_score: float, emotion_magnitude: float) -> Statistics:
    """
    Save new statistics to the database.
    
    Args:
        user (User): User object
        emotion_score (float): Emotion score
        emotion_magnitude (float): Emotion magnitude
        
    Returns:
        Statistics: Created statistics object
    """
    statistics = Statistics.objects.create(
        user=user,
        emotion_score=emotion_score,
        emotion_magnitude=emotion_magnitude
    )
    return statistics

def gather_user_statistics(user: User) -> Dict[str, Any]:
    """
    Get comprehensive user statistics.
    
    Args:
        user (User): User object
        
    Returns:
        Dict[str, Any]: Dictionary containing various statistics
    """
    try:
        emotion_data_qs = Statistics.objects.filter(user=user)
        
        # Basic statistics calculations
        emotion_scores = list(emotion_data_qs.values_list("emotion_score", flat=True))
        emotion_magnitudes = list(emotion_data_qs.values_list("emotion_magnitude", flat=True))
        
        # Daily and weekly statistics with optimized queries
        daily_emotion_stats = _get_daily_stats(emotion_data_qs)
        weekly_emotion_stats = _get_weekly_stats(emotion_data_qs)
        
        # Summary of ChatMessage per day
        daily_chat_stats = _get_daily_chat_stats()
        weekly_chat_stats = _get_weekly_chat_stats()
        
        # Sentiment classification
        sentiment_stats = _calculate_sentiment_statistics(
            emotion_data_qs,
            SENTIMENT_THRESHOLDS
        )
        
        # Statistical analysis
        statistical_analysis = _perform_statistical_analysis(
            emotion_scores,
            emotion_magnitudes
        )
        
        return {
            **sentiment_stats,
            **statistical_analysis,
            "daily_chat_stats": daily_chat_stats,
            "weekly_chat_stats": weekly_chat_stats,
            "scatter_data": list(zip(emotion_scores, emotion_magnitudes)),
            "daily_emotion_stats": daily_emotion_stats,
            "weekly_emotion_stats": weekly_emotion_stats,
        }
    except Exception as e:
        logger.error(f"Error gathering user statistics: {e}")
        raise

def _get_daily_stats(queryset) -> List[Dict]:
    """Helper function for daily statistics calculation"""
    return list(
        queryset
        .annotate(date=TruncDay("created_at"))
        .values("date")
        .annotate(avg_score=Avg("emotion_score"), count=Count("id"))
        .order_by("date")
    )

def _get_weekly_stats(queryset) -> List[Dict]:
    """Helper function for weekly statistics calculation"""
    return list(
        queryset
        .annotate(week=TruncWeek("created_at"))
        .values("week")
        .annotate(avg_score=Avg("emotion_score"), count=Count("id"))
        .order_by("week")
    )

def _get_daily_chat_stats() -> List[Dict]:
    """Helper function for daily chat statistics calculation"""
    return list(
        ChatMessage.objects
        .annotate(date=TruncDay("created_at"))
        .values("date")
        .annotate(total_messages=Count("id"))
        .order_by("date")
    )

def _get_weekly_chat_stats() -> List[Dict]:
    """Helper function for weekly chat statistics calculation"""
    return list(
        ChatMessage.objects
        .annotate(week=TruncWeek("created_at"))
        .values("week")
        .annotate(total_messages=Count("id"))
        .order_by("week")
    )

def _calculate_sentiment_statistics(queryset, thresholds: Dict) -> Dict:
    """Helper function for sentiment classification"""
    daily_sentiment_classification = (
        queryset
        .annotate(date=TruncDay("created_at"))
        .values("date")
        .annotate(
            positive=Count("id", filter=Q(emotion_score__gt=thresholds['POSITIVE'])),
            negative=Count("id", filter=Q(emotion_score__lt=thresholds['NEGATIVE'])),
            neutral=Count("id", filter=Q(emotion_score__gte=thresholds['NEUTRAL_MIN'], emotion_score__lte=thresholds['NEUTRAL_MAX'])),
            mixed=Count(
                "id",
                filter=Q(
                    emotion_score__gt=thresholds['NEUTRAL_MIN'],
                    emotion_score__lt=thresholds['NEUTRAL_MAX'],
                    emotion_magnitude__gt=thresholds['MIXED_MAGNITUDE']
                )
            ),
        )
        .order_by("date")
    )

    weekly_sentiment_classification = (
        queryset
        .annotate(week=TruncWeek("created_at"))
        .values("week")
        .annotate(
            positive=Count("id", filter=Q(emotion_score__gt=thresholds['POSITIVE'])),
            negative=Count("id", filter=Q(emotion_score__lt=thresholds['NEGATIVE'])),
            neutral=Count("id", filter=Q(emotion_score__gte=thresholds['NEUTRAL_MIN'], emotion_score__lte=thresholds['NEUTRAL_MAX'])),
            mixed=Count(
                "id",
                filter=Q(
                    emotion_score__gt=thresholds['NEUTRAL_MIN'],
                    emotion_score__lt=thresholds['NEUTRAL_MAX'],
                    emotion_magnitude__gt=thresholds['MIXED_MAGNITUDE']
                )
            ),
        )
        .order_by("week")
    )

    return {
        "daily_sentiment_classification": list(daily_sentiment_classification),
        "weekly_sentiment_classification": list(weekly_sentiment_classification),
    }

def _perform_statistical_analysis(scores: List[float], magnitudes: List[float]) -> Dict:
    """Helper function for statistical analysis"""
    # Initialize with None to indicate undefined values
    correlation_score_magnitude = None
    skewness_value = None
    kurtosis_value = None
    descriptive_skewness = "undefined"
    descriptive_kurtosis = "undefined"

    if len(scores) > 1:
        # Check if all scores are identical
        if len(set(scores)) > 1:
            try:
                corr, _ = stats.pearsonr(scores, magnitudes)
                correlation_score_magnitude = corr if not math.isnan(corr) else None
            except Exception as e:
                correlation_score_magnitude = None

            try:
                skew = stats.skew(scores)
                skewness_value = skew if not math.isnan(skew) else None
            except Exception as e:
                skewness_value = None

            try:
                kurt = stats.kurtosis(scores)
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

    return {
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
