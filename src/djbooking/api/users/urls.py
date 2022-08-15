from django.urls import path

from djbooking.api.users.views import UserLoginAPIView

app_name = "users"

urlpatterns = [path("login/", UserLoginAPIView.as_view(), name="user-login")]
