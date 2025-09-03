from django.core.exceptions import ValidationError
from django.conf import settings
from zxcvbn import zxcvbn

class PasswordStrengthValidator:
    """
    Enhanced password strength validator using zxcvbn library.
    Provides detailed feedback and user context awareness.
    """
    
    def __init__(self, min_score=2):
        self.min_score = min_score
    
    def validate(self, password, user=None):
        # Prepare user inputs for zxcvbn to check against
        user_inputs = []
        if user:
            if hasattr(user, 'email') and user.email:
                user_inputs.extend([user.email, user.email.split('@')[0]])
            if hasattr(user, 'name') and user.name:
                user_inputs.append(user.name)
        
        # Analyze password strength
        results = zxcvbn(password, user_inputs=user_inputs)
        
        if results['score'] < self.min_score:
            # Generate detailed error message
            error_message = self._get_detailed_error_message(results)
            raise ValidationError(
                error_message,
                code='password_too_weak',
            )
    
    def _get_detailed_error_message(self, results):
        """
        Generate detailed error message based on zxcvbn feedback.
        Uses Japanese since LANGUAGE_CODE = "ja" in settings.
        """
        score = results['score']
        feedback = results.get('feedback', {})
        warning = feedback.get('warning', '')
        suggestions = feedback.get('suggestions', [])
        
        # Base message in Japanese
        if score == 0:
            base_msg = "パスワードが非常に弱いです。"
        elif score == 1:
            base_msg = "パスワードが弱いです。"
        else:
            base_msg = "パスワードの強度が不十分です。"
        
        # Add warning if available
        warning_translations = {
            'This is a top-10 common password': 'これは一般的によく使われるパスワードです。',
            'This is a top-100 common password': 'これは一般的によく使われるパスワードです。',
            'This is a very common password': 'これは非常に一般的なパスワードです。',
            'This is similar to a commonly used password': 'これは一般的なパスワードに似ています。',
            'A word by itself is easy to guess': '単語だけのパスワードは推測されやすいです。',
            'Names and surnames by themselves are easy to guess': '名前や姓だけのパスワードは推測されやすいです。',
            'Common names and surnames are easy to guess': '一般的な名前は推測されやすいです。',
            'Straight rows of keys are easy to guess': 'キーボードの連続した配列は推測されやすいです。',
            'Short keyboard patterns are easy to guess': '短いキーボードパターンは推測されやすいです。',
            'Repeats like "aaa" are easy to guess': '"aaa"のような繰り返しは推測されやすいです。',
            'Repeats like "abcabcabc" are only slightly harder to guess than "abc"': '"abcabcabc"のような繰り返しは"abc"より少し複雑な程度です。',
            'Sequences like abc or 6543 are easy to guess': 'abcや6543のような連続は推測されやすいです。',
            'Recent years are easy to guess': '最近の年号は推測されやすいです。',
            'Dates are often easy to guess': '日付は推測されやすいです。'
        }
        
        if warning and warning in warning_translations:
            base_msg += f" {warning_translations[warning]}"
        
        # Add suggestions
        suggestion_translations = {
            'Add another word or two. Uncommon words are better.': '単語を追加してください。一般的でない単語の方が良いです。',
            'Use a longer keyboard pattern with more turns.': 'より長く複雑なキーボードパターンを使用してください。',
            'Avoid repeated words and characters.': '同じ単語や文字の繰り返しを避けてください。',
            'Avoid sequences.': '連続した文字や数字を避けてください。',
            'Avoid recent dates and years.': '最近の日付や年号を避けてください。',
            'Avoid years that are associated with you.': 'あなたに関連する年号を避けてください。',
            'Avoid dates and years that are associated with you.': 'あなたに関連する日付や年号を避けてください。',
            'Capitalization doesn\'t help very much.': '大文字化だけでは十分ではありません。',
            'All-uppercase is almost as easy to guess as all-lowercase.': 'すべて大文字でもすべて小文字でも推測の難易度はほぼ同じです。',
            'Reversed words aren\'t much harder to guess.': '逆さまの単語でも推測の難易度はあまり変わりません。',
            'Predictable substitutions like \'@\' instead of \'a\' don\'t help very much.': '\'a\'を\'@\'に置き換えるような予測可能な置換は効果的ではありません。'
        }
        
        if suggestions:
            base_msg += " 改善案: "
            translated_suggestions = []
            for suggestion in suggestions:
                if suggestion in suggestion_translations:
                    translated_suggestions.append(suggestion_translations[suggestion])
                else:
                    translated_suggestions.append(suggestion)
            base_msg += " ".join(translated_suggestions)
        
        if not suggestions and not warning:
            base_msg += " より長く複雑なパスワードを使用してください。大文字・小文字・数字・記号を組み合わせることをお勧めします。"
        
        return base_msg
    
    def get_help_text(self):
        return "パスワードは十分に強力である必要があります。推測されにくいパスワードを選択してください。"
