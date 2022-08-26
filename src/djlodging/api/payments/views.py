from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ViewSet

from djlodging.api.payments.serializers import (
    PaymentIntentCreateInputSerializer,
    PaymentIntentCreateOutputSerializer,
)
from djlodging.application_services.payments import PaymentService


class PaymentViewSet(ViewSet):
    @action(detail=False, methods=["post"])
    def pay(self, request):
        input_serializer = PaymentIntentCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        client_secret = PaymentService.pay(user=request.user, **input_serializer.validated_data)
        output_serializer = PaymentIntentCreateOutputSerializer({"client_secret": client_secret})
        return Response(data=output_serializer.data, status=HTTP_201_CREATED)
