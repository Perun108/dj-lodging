from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.views import TokenViewBase

from djlodging.api.users.serializers import (
    ForgotPasswordInputSerializer,
    PartnerCreateInputSerializer,
    PasswordChangeInputSerializer,
    PasswordResetInputSerializer,
    UserLoginOutputSerializer,
    UserOutputSerializer,
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
        output_serializer = UserShortOutputSerializer(user)
        return Response(output_serializer.data, status=HTTP_201_CREATED)


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


class PasswordChangeAPIView(APIView):
    def patch(self, request):
        input_serializer = PasswordChangeInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        UserService.change_password(user=request.user, **input_serializer.validated_data)
        return Response(status=HTTP_200_OK)


class ForgotPasswordAPIView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        incoming_data = ForgotPasswordInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        UserService.send_forgot_password_link(**incoming_data.validated_data)
        return Response(status=HTTP_202_ACCEPTED)


class PasswordResetAPIView(APIView):
    """
    API to confirm that there is such user with this security token.

    This is the second step of 'forgot password' flow.
    This API should be used after ForgotPasswordAPIView where a token is sent
    to an email specified by user.

    To complete resetting password in the 'forgot password' flow - use the third step
    PasswordChangeAPIView (login user with the old_password and change it to the new_password)
    """

    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        incoming_data = PasswordResetInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        UserService.confirm_reset_password(**incoming_data.validated_data)
        return Response(status=HTTP_200_OK)


class UserViewSet(ViewSet):
    # def update(self, request):
    # incoming_data = UserUpdateInputSerializer(data=request.data)
    # incoming_data.is_valid(raise_exception=True)
    # UserService.update(**incoming_data.validated_data)
    # return Response(status=HTTP_201_CREATED)
    # pass

    @action(methods=["patch"], detail=True)
    def partner(self, request, pk):
        if str(request.user.id) != pk:
            raise PermissionDenied
        input_serializer = PartnerCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        partner = UserService.make_user_partner(
            actor=request.user, user_id=pk, **input_serializer.validated_data
        )
        output_serializer = UserOutputSerializer(partner)
        return Response(data=output_serializer.data, status=HTTP_200_OK)
