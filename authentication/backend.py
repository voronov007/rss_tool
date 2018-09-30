from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            logged_in = user.check_password(password)
            if logged_in:
                return user
        except User.DoesNotExist:
            return

        return
