import re

from django.http import HttpResponseRedirect
from django.shortcuts import reverse

from sendcloud.settings import LOGIN_REDIRECT_URL


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_login = re.match(r"^(\/login\/?)$", request.path)
        is_register = re.match(r"^(\/register\/?)$", request.path)
        is_admin = re.match(r"^(\/admin\/?)", request.path)
        if request.user.is_authenticated:
            if any([is_login, is_register]):
                return HttpResponseRedirect(LOGIN_REDIRECT_URL)
        else:
            # access  only for login
            if not any([is_login, is_admin, is_register]):
                return HttpResponseRedirect(reverse("login"))

        response = self.get_response(request)
        return response
