from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class UsernameOrEmailBackend(ModelBackend):
    """
    Authentifiziert Benutzer über Username oder E-Mail.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        if user.check_password(password):
            return user
        return None


