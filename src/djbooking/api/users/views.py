from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.views import TokenViewBase

from djbooking.api.users.serializers import (
    UserCreateInputSerializer,
    UserLoginOutputSerializer,
)
from djbooking.application_services.users import UserService


class UserLoginAPIView(TokenViewBase):
    serializer_class = UserLoginOutputSerializer


class UserViewSet(ViewSet):
    def create(self, request):
        incoming_data = UserCreateInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        UserService.create(**incoming_data.validated_data, is_active=False)
        return Response(status=HTTP_201_CREATED)
