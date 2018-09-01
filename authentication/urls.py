from django.contrib import admin
from django.urls import path, include, re_path

from .views import UserFormView, UserRegisterView

urlpatterns = [
    re_path('login/?', UserFormView.as_view(), name='login'),
    re_path('register/?', UserRegisterView.as_view(), name='register'),
]
