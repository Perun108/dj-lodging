from django.urls import path

from djlodging.api.users.views import (
    UserLoginAPIView,
    UserRegistrationConfirmAPIView,
    UserSingUpAPIView,
)

app_name = "users"

urlpatterns = [
    path("sign-up/", UserSingUpAPIView.as_view(), name="sign-up"),
    path("registration/", UserRegistrationConfirmAPIView.as_view(), name="registration"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
]
