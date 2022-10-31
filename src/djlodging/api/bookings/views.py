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
    BookingListPaginatedOutputSerializer,
    BookingOutputSerializer,
    BookingPayInputSerializer,
)
from djlodging.application_services.bookings import BookingService


class BookingViewSet(ViewSet):
    @extend_schema(
        request=None,
        responses={200: BookingListPaginatedOutputSerializer},
        summary="List all bookings by admin (filtered)",
        parameters=[
            OpenApiParameter(
                "user_id",
                OpenApiTypes.UUID,
                OpenApiParameter.QUERY,
                description=("Filter by user's id"),
            ),
            OpenApiParameter(
                "date_from",
                OpenApiTypes.DATE,
                OpenApiParameter.QUERY,
                description=("Filter by date_from - gte"),
            ),
            OpenApiParameter(
                "date_to",
                OpenApiTypes.DATE,
                OpenApiParameter.QUERY,
                description=("Filter by date_to - lte"),
            ),
            OpenApiParameter(
                "status",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=("Filter by status"),
            ),
            OpenApiParameter(
                "lodging_id",
                OpenApiTypes.UUID,
                OpenApiParameter.QUERY,
                description=("Filter by lodging_id"),
            ),
            OpenApiParameter(
                "owner_id",
                OpenApiTypes.UUID,
                OpenApiParameter.QUERY,
                description=("Filter by owner_id"),
            ),
            OpenApiParameter(
                "kind",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=("Filter by kind"),
            ),
            OpenApiParameter(
                "country_name",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=("Filter by country_name"),
            ),
            OpenApiParameter(
                "region_name",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=("Filter by region_name"),
            ),
            OpenApiParameter(
                "city_name",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=("Filter by city_name"),
            ),
            OpenApiParameter(
                "city_district",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=("Filter by city_district"),
            ),
            OpenApiParameter(
                "street",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=("Filter by street"),
            ),
            OpenApiParameter(
                "zip_code",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=("Filter by zip_code"),
            ),
            OpenApiParameter(
                "email",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=("Filter by email"),
            ),
            OpenApiParameter(
                "number_of_people",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description=("Filter by number_of_people"),
            ),
            OpenApiParameter(
                "number_of_rooms",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description=("Filter by number_of_rooms"),
            ),
            OpenApiParameter(
                "price_gte",
                OpenApiTypes.DECIMAL,
                OpenApiParameter.QUERY,
                description=("Filter by price_gte"),
            ),
            OpenApiParameter(
                "price_lte",
                OpenApiTypes.DECIMAL,
                OpenApiParameter.QUERY,
                description=("Filter by price_lte"),
            ),
        ],
    )
    def list(self, request):
        bookings = BookingService.get_filtered_paginated_list(
            actor=request.user, query_params=request.query_params
        )
        output_serializer = BookingListPaginatedOutputSerializer(bookings)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH)
        ],
        request=None,
        responses={
            200: BookingOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Retrieve a booking details by admin",
    )
    def retrieve(self, request, pk):
        booking = BookingService.retrieve(actor=request.user, booking_id=pk)
        output_serializer = BookingOutputSerializer(booking)
        return Response(data=output_serializer.data, status=HTTP_200_OK)


class MyBookingViewSet(ViewSet):
    @extend_schema(
        request=BookingCreateInputSerializer,
        responses={
            201: BookingOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Book a lodging",
    )
    def create(self, request):
        input_serializer = BookingCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        booking = BookingService.create(user=request.user, **input_serializer.validated_data)
        output_serializer = BookingOutputSerializer(booking)
        return Response(data=output_serializer.data, status=HTTP_201_CREATED)

    @extend_schema(
        request=None,
        responses={200: BookingListPaginatedOutputSerializer},
        summary="List my bookings",
    )
    def list(self, request):
        """
        List my bookings.
        """
        bookings = BookingService.get_my_paginated_list(
            user=request.user, query_params=request.query_params
        )
        output_serializer = BookingListPaginatedOutputSerializer(bookings)
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
        summary="Pay for booking",
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
        summary="Cancel a booking",
    )
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk):
        booking = BookingService.cancel(actor=request.user, booking_id=pk)
        output_serializer = BookingOutputSerializer(booking)
        return Response(output_serializer.data, status=HTTP_200_OK)
