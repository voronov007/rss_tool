from django.urls import re_path

from .views import UserLoginView, UserRegisterView

urlpatterns = [
    re_path("login/?", UserLoginView.as_view(), name="login"),
    re_path("register/?", UserRegisterView.as_view(), name="register"),
]
