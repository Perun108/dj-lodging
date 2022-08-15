import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture()
def user():
    email = "example@example.com"
    password = "1234"
    user = User.objects.create(email=email, password=password)
    user.set_password(password)
    user.save()
    return user
