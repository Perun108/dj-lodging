from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.viewsets import ViewSet

from djlodging.api.bookings.serializers import (
    BookingCreateInputSerializer,
    BookingCreateOutputSerializer,
    BookingListOutputSerializer,
)
from djlodging.application_services.bookings import BookingService
from djlodging.domain.bookings.repository import BookingRepository


class BookingViewSet(ViewSet):
    @extend_schema(
        request=BookingCreateInputSerializer,
        responses={
            201: BookingCreateOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def create(self, request):
        input_serializer = BookingCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        booking = BookingService.create(user=request.user, **input_serializer.validated_data)
        output_serializer = BookingCreateOutputSerializer(booking)
        return Response(data=output_serializer.data, status=HTTP_201_CREATED)

    @extend_schema(
        request=None,
        responses={200: BookingListOutputSerializer},
    )
    def list(self, request):
        bookings = BookingRepository.get_list(user=request.user)
        output_serializer = BookingListOutputSerializer(bookings, many=True)
        return Response(data=output_serializer.data, status=HTTP_200_OK)
