from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.views import TokenViewBase

from djlodging.api.users.serializers import (
    EmailChangeConfirmInputSerializer,
    EmailChangeRequestInputSerializer,
    PartnerCreateInputSerializer,
    PasswordChangeInputSerializer,
    PasswordResetConfirmInputSerializer,
    SendForgotPasswordInputSerializer,
    UserLoginOutputSerializer,
    UserOutputSerializer,
    UserRegistrationConfirmInputSerializer,
    UserShortOutputSerializer,
    UserSignUpInputSerializer,
    UserUpdateInputSerializer,
)
from djlodging.application_services.email import EmailService
from djlodging.application_services.users import UserService
from djlodging.domain.users.repository import UserRepository


class UserSingUpAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()

    @extend_schema(
        request=UserSignUpInputSerializer,
        responses={
            201: UserShortOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Sign up",
    )
    def post(self, request):
        """
        is_user corresponds to "Do you plan to rent listed properties?"
        is_partner corresponds to "Do you plan to list property for rent?"

        """
        incoming_data = UserSignUpInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        user = UserService.create(**incoming_data.validated_data, is_active=False)
        EmailService.send_confirmation_link(user.email, user.security_token)
        output_serializer = UserShortOutputSerializer(user)
        return Response(output_serializer.data, status=HTTP_201_CREATED)


class UserGetByTokenAndEmailAPIView(APIView):
    """
    API to check if a user with such security token and email exists.

    This is an intermediate API just for FE side verifications
    before registration-confirm, password-forget-reset or email-change flows.

    If a token/email is wrong - just display an error to a user and no need to collect their
    password/email to change.

    If a user exists - proceed further to confirm registration or collect
    their email/password to change.
    """

    permission_classes = ()
    authentication_classes = ()

    @extend_schema(
        parameters=[
            OpenApiParameter("token", type=OpenApiTypes.UUID, location=OpenApiParameter.QUERY),
            OpenApiParameter("email", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        ],
        responses={
            200: inline_serializer(
                name="retrieve_user_id",
                fields={"user_id": serializers.UUIDField()},
            ),
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Get user by security token and email",
    )
    def get(self, request):
        token = request.query_params.get("token")
        email = request.query_params.get("email")
        user = UserRepository.get_user_by_security_token_and_email(token, email)
        return Response({"user_id": user.id}, status=HTTP_200_OK)


class UserRegistrationConfirmAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()

    @extend_schema(
        request=UserRegistrationConfirmInputSerializer,
        responses={
            200: None,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Confirm registration",
    )
    def post(self, request):
        incoming_data = UserRegistrationConfirmInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        UserService.confirm_registration(**incoming_data.validated_data)
        return Response(status=HTTP_200_OK)


class UserLoginAPIView(TokenViewBase):
    serializer_class = UserLoginOutputSerializer


class PasswordChangeAPIView(APIView):
    @extend_schema(
        request=PasswordChangeInputSerializer,
        responses={
            200: None,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Change password",
    )
    def patch(self, request):
        input_serializer = PasswordChangeInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        UserService.change_password(user=request.user, **input_serializer.validated_data)
        return Response(status=HTTP_200_OK)


class SendForgotPasswordLinkAPIView(APIView):
    permission_classes = ()
    authentication_classes = ()

    @extend_schema(
        request=SendForgotPasswordInputSerializer,
        responses={
            202: None,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Send forgot password link",
    )
    def post(self, request):
        incoming_data = SendForgotPasswordInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        UserService.send_forgot_password_link(**incoming_data.validated_data)
        return Response(status=HTTP_202_ACCEPTED)


class PasswordResetConfirmAPIView(APIView):
    """
    This is the second step of 'forgot password' flow.
    This API should be used after SendForgotPasswordLinkAPIView where a token is sent
    to an email specified by user.

    After a user resets his/her password via this API they should be logged in via UserLoginAPI.
    """

    permission_classes = ()
    authentication_classes = ()

    @extend_schema(
        request=PasswordResetConfirmInputSerializer,
        responses={
            200: None,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Confirm resetting password after forgetting",
    )
    def post(self, request):
        incoming_data = PasswordResetConfirmInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        UserService.confirm_reset_password(**incoming_data.validated_data)
        return Response(status=HTTP_200_OK)


class EmailChangeRequestAPIView(APIView):
    @extend_schema(
        request=EmailChangeRequestInputSerializer,
        responses={202: None},
        summary="Send a link to new email",
    )
    def post(self, request):
        input_serializer = EmailChangeRequestInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        UserService.send_change_email_link(user=request.user, **input_serializer.validated_data)
        return Response(status=HTTP_202_ACCEPTED)


class EmailChangeConfirmAPIView(APIView):
    permission_classes = ()
    authentication_classes = ()

    @extend_schema(
        request=EmailChangeConfirmInputSerializer,
        responses={200: None},
        summary="Confirm change email",
    )
    def post(self, request):
        input_serializer = EmailChangeConfirmInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        UserService.change_email(**input_serializer.validated_data)
        return Response(status=HTTP_200_OK)


class UserViewSet(ViewSet):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="user_id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH
            )
        ],
        request=UserUpdateInputSerializer,
        responses={
            200: UserOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Update user by admin",
    )
    def update(self, request, pk):
        """
        Update a user by admin. Different from the 'update_me' method.
        """
        incoming_data = UserUpdateInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        user = UserService.update_by_admin(
            actor=request.user, user_id=pk, **incoming_data.validated_data
        )
        output_serializer = UserOutputSerializer(user)
        return Response(output_serializer.data, status=HTTP_200_OK)


class MeViewSet(ViewSet):
    @extend_schema(
        request=PartnerCreateInputSerializer,
        responses={
            200: UserOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Make me a partner",
    )
    @action(methods=["patch"], detail=False, url_path="me/partner")
    def create_partner(self, request):
        """
        Update a user to make him/her a partner who can manage and rent lodgings out.
        """
        input_serializer = PartnerCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        partner = UserService.make_user_partner(
            user=request.user, **input_serializer.validated_data
        )
        output_serializer = UserOutputSerializer(partner)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        request=None,
        responses={
            200: UserOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        methods=["GET"],
        description="Retrieve a user by himself. Different from the plain 'retrieve' method.",
        summary="Get my details",
    )
    @extend_schema(
        request=UserUpdateInputSerializer,
        responses={
            200: UserOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        methods=["PUT"],
        description="Update a user by himself. Different from the plain 'update' method.",
        summary="Update my details",
    )
    @action(detail=False, methods=["get", "put"])
    def me(self, request):
        """
        Retrieve/Update a user by himself. Different from the plain 'retrieve/update' method.
        """
        if request.method == "GET":
            output_serializer = UserOutputSerializer(request.user)
            return Response(output_serializer.data, status=HTTP_200_OK)

        elif request.method == "PUT":
            incoming_data = UserUpdateInputSerializer(data=request.data)
            incoming_data.is_valid(raise_exception=True)
            user = UserService.update(user=request.user, **incoming_data.validated_data)
            output_serializer = UserOutputSerializer(user)
            return Response(output_serializer.data, status=HTTP_200_OK)
