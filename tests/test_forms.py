import pytest

from django.contrib.auth.models import User

from authentication.forms import UserLoginForm, UserRegisterForm

pytestmark = pytest.mark.django_db


def test_user_form_ok():
    email = "test@test.com"
    password = "test1234"
    form = UserLoginForm({"email": email, "password": password})
    assert form.is_valid() is True


def test_user_form_error():
    email = "test@test.com"
    password = "test123"
    form = UserLoginForm({"email": email, "password": password})
    assert form.is_valid() is False

    email = "test"
    password = "test124"
    form = UserLoginForm({"email": email, "password": password})
    assert form.is_valid() is False


def test_user_register_form_error():
    email = "test@test.com"
    password = "test1234"
    user = User.objects.create(email=email, password=password, username=email)

    form = UserRegisterForm({"email": email, "password": password})
    assert form.is_valid() is False


def test_user_register_form_ok():
    email = "test@test.com"
    password = "test1234"

    form = UserRegisterForm({"email": email, "password": password})
    assert form.is_valid() is True
