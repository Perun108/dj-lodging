from django.urls import path

from djlodging.api.users.views import (
    ForgotPasswordAPIView,
    PasswordChangeAPIView,
    UserLoginAPIView,
    UserRegistrationConfirmAPIView,
    UserSingUpAPIView,
)

app_name = "users"

urlpatterns = [
    path("sign-up/", UserSingUpAPIView.as_view(), name="sign-up"),
    path("registration/", UserRegistrationConfirmAPIView.as_view(), name="registration"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path(
        "password-change/",
        PasswordChangeAPIView.as_view(),
        name="change-password",
    ),
    path(
        "password-forgot/",
        ForgotPasswordAPIView.as_view(),
        name="forgot-password",
    ),
    # path("password-confirm/", PasswordChangeInitializeAPIView.as_view(), name="change-password"),
]
