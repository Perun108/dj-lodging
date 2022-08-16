from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserLoginOutputSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["username"] = self.user.full_name
        return data


class UserCreateInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
