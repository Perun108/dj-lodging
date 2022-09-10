from rest_framework import serializers


class PaymentIntentCreateInputSerializer(serializers.Serializer):
    currency = serializers.CharField(required=False)
    capture_method = serializers.CharField(required=False)
    metadata = serializers.DictField(child=serializers.CharField())


class PaymentIntentCreateOutputSerializer(serializers.Serializer):
    client_secret = serializers.CharField()
