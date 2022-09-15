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
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.viewsets import ViewSet

from djlodging.api.bookings.serializers import (
    BookingCreateInputSerializer,
    BookingListOutputSerializer,
    BookingOutputSerializer,
    BookingPayInputSerializer,
)
from djlodging.application_services.bookings import BookingService
from djlodging.domain.bookings.repository import BookingRepository


class BookingViewSet(ViewSet):
    @extend_schema(
        request=BookingCreateInputSerializer,
        responses={
            201: BookingOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def create(self, request):
        input_serializer = BookingCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        booking = BookingService.create(user=request.user, **input_serializer.validated_data)
        output_serializer = BookingOutputSerializer(booking)
        return Response(data=output_serializer.data, status=HTTP_201_CREATED)

    @extend_schema(
        request=None,
        responses={200: BookingListOutputSerializer},
    )
    def list(self, request):
        bookings = BookingRepository.get_list(user=request.user)
        output_serializer = BookingListOutputSerializer(bookings, many=True)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH)
        ],
        request=BookingPayInputSerializer,
        responses={
            201: inline_serializer(
                name="pay_for_booking", fields={"client_secret": serializers.CharField()}
            ),
            400: OpenApiResponse(description="Bad request"),
        },
    )
    @action(detail=True, methods=["post"])
    def pay(self, request, pk):
        input_serializer = BookingPayInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        client_secret = BookingService.pay(
            actor=request.user, booking_id=pk, **input_serializer.validated_data
        )
        return Response({"client_secret": client_secret}, status=HTTP_201_CREATED)

    @extend_schema(
        parameters=[
            OpenApiParameter("id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH)
        ],
        request=None,
        responses={
            200: BookingOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
    )
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk):
        booking = BookingService.cancel(actor=request.user, booking_id=pk)
        output_serializer = BookingOutputSerializer(booking)
        return Response(output_serializer.data, status=HTTP_200_OK)
