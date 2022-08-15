from rest_framework_simplejwt.views import TokenViewBase

from djbooking.api.users.serializers import UserLoginOutputSerializer


class UserLoginAPIView(TokenViewBase):
    serializer_class = UserLoginOutputSerializer
    # permission_classes = ()
    # authentication_classes = ()
