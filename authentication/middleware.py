import re

from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.utils.deprecation import MiddlewareMixin
from sendcloud.settings import LOGIN_REDIRECT_URL


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        is_login = re.match(r'^(\/login\/?)$', request.path)
        is_register = re.match(r'^(\/register\/?)$', request.path)
        is_admin = re.match(r'^(\/admin\/?)', request.path)
        if request.user.is_authenticated:
            if any([is_login, is_register]):
                return HttpResponseRedirect(LOGIN_REDIRECT_URL)
            return
        else:
            # access  only for login
            if not any([is_login, is_admin, is_register]):
                return HttpResponseRedirect(reverse('login'))
