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
    registration_token = serializers.UUIDField()


class UserShortOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()


class PartnerCreateInputSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)


class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
