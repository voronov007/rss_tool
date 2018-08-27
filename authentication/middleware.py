import re

from django.http import HttpResponseRedirect
from django.shortcuts import reverse

from django.contrib.auth import authenticate, login
from django.http.response import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            return
        else:
            # access  only for login
            is_admin = re.match(r'^(\/admin\/?)', request.path)
            is_login = re.match(r'^(\/login\/?)$', request.path)
            if not any([is_login, is_admin]):
                return HttpResponseRedirect(reverse('login'))
