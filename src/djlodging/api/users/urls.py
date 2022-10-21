from django.urls import path

from djlodging.api.users.views import (  # UserGetByTokenAndEmailAPIView,
    EmailChangeConfirmAPIView,
    EmailChangeRequestAPIView,
    PasswordChangeAPIView,
    PasswordResetConfirmAPIView,
    SendForgotPasswordLinkAPIView,
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
        SendForgotPasswordLinkAPIView.as_view(),
        name="forgot-password",
    ),
    path(
        "password-reset-confirmation/",
        PasswordResetConfirmAPIView.as_view(),
        name="confirm-reset-password",
    ),
    path(
        "email-change-request/",
        EmailChangeRequestAPIView.as_view(),
        name="request-change-email",
    ),
    path(
        "email-change-confirm/",
        EmailChangeConfirmAPIView.as_view(),
        name="confirm-change-email",
    ),
    # path(
    #     "id/",
    #     UserGetByTokenAndEmailAPIView.as_view(),
    #     name="get-user-id",
    # ),
]
