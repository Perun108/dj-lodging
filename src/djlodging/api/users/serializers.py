from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserLoginOutputSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["username"] = self.user.full_name
        data["user_id"] = self.user.id
        data["is_user"] = self.user.is_user
        data["is_partner"] = self.user.is_partner
        return data


class UserSignUpInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserRegistrationConfirmInputSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    security_token = serializers.UUIDField()


class PasswordChangeInputSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class SendForgotPasswordInputSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmInputSerializer(serializers.Serializer):
    security_token = serializers.UUIDField()
    email = serializers.EmailField()
    new_password = serializers.CharField()


class EmailChangeRequestInputSerializer(serializers.Serializer):
    new_email = serializers.EmailField()


class EmailChangeConfirmInputSerializer(serializers.Serializer):
    security_token = serializers.UUIDField()
    new_email = serializers.EmailField()


class UserShortOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()


class PartnerCreateInputSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)


class UserOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    date_of_birth = serializers.DateField()
    nationality = serializers.CharField()
    gender = serializers.CharField()
    is_superuser = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    is_user = serializers.BooleanField()
    is_partner = serializers.BooleanField()


class LodgingUserOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
