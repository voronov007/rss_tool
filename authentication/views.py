from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, reverse
from django.views import View
from django.http import HttpResponseRedirect

from sendcloud.settings import LOGIN_REDIRECT_URL

from .forms import UserLoginForm, UserRegisterForm


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        data = {
            'form': form
        }
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(LOGIN_REDIRECT_URL)
            else:
                data["error"] = "Incorrect email or password!"
                render(request, self.template_name, data)

        return render(request, self.template_name, data)


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'authentication/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        data = {
            'form': form
        }
        if not form.is_valid():
            return render(request, self.template_name, data)

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        try:
            new_user = User.objects.create_user(
                username=email, email=email, password=password
            )
        except Exception as e:
            data["error"] = "Incorrect user credentials were provided."
            return render(request, self.template_name, data)

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(LOGIN_REDIRECT_URL)

