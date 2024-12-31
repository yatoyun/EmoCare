from django.contrib.auth import authenticate

from apps.users.models import User

def register_user(name: str, email: str, password: str) -> User:
    # check if email is already registered
    if User.objects.filter(email=email).exists():
        raise ValueError("Email already registered")

    user = User.objects.create_user(
        name=name,
        email=email,
        password=password
    )
    return user

# FIXME
# use raise ValueError instead of return None
def login_user(name: str = None, email: str = None, password: str = None) -> User:
    if name and not email:
        try:
            user_obj = User.objects.get(name=name)
            if user_obj.check_password(password):
                return user_obj
            else:
                return None
        except User.DoesNotExist:
            return None

    # email で認証する処理 username に email をセット
    if email and not name:
        user = authenticate(username=email, password=password)
        return user

    return None
