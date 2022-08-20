from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.views import TokenViewBase

from djlodging.api.users.serializers import (
    UserLoginOutputSerializer,
    UserRegistrationConfirmInputSerializer,
    UserShortOutputSerializer,
    UserSignUpInputSerializer,
)
from djlodging.application_services.email import EmailService
from djlodging.application_services.users import UserService


class UserSingUpAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
        is_user corresponds to "Do you plan to rent listed properties?"
        is_partner corresponds to "Do you plan to list property for rent?"

        """
        incoming_data = UserSignUpInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        user = UserService.create(**incoming_data.validated_data, is_active=False)
        EmailService.send_confirmation_link(user.id)
        return Response(status=HTTP_201_CREATED)


class UserRegistrationConfirmAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        incoming_data = UserRegistrationConfirmInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        user = UserService.confirm_registration(**incoming_data.validated_data)
        outgoing_data = UserShortOutputSerializer(user)
        return Response(data=outgoing_data.data, status=HTTP_200_OK)


class UserLoginAPIView(TokenViewBase):
    serializer_class = UserLoginOutputSerializer


class UserViewSet(ViewSet):
    def update(self, request):
        # incoming_data = UserUpdateInputSerializer(data=request.data)
        # incoming_data.is_valid(raise_exception=True)
        # UserService.update(**incoming_data.validated_data)
        # return Response(status=HTTP_201_CREATED)
        pass
