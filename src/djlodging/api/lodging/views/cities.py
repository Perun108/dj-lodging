"""API module for the management of cities."""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ViewSet

from djlodging.api.lodging.serializers import (
    CityCreateInputSerializer,
    CityListPaginatedOutputSerializer,
    CityOutputSerializer,
    CityUpdateInputSerializer,
)
from djlodging.application_services.lodgings import CityService


class CityViewSet(ViewSet):
    """ViewSet for the cities APIs."""

    permission_classes = (IsAdminUser,)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="country_id", type=OpenApiTypes.STR, location=OpenApiParameter.PATH
            )
        ],
        request=CityCreateInputSerializer,
        responses={
            201: CityOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Add a city by admin",
    )
    def create(self, request, country_pk):
        """Create a new city."""
        incoming_data = CityCreateInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        city = CityService.create(
            actor=request.user, country_id=country_pk, **incoming_data.validated_data
        )
        output_serializer = CityOutputSerializer(city)
        return Response(data=output_serializer.data, status=HTTP_201_CREATED)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="country_id", type=OpenApiTypes.STR, location=OpenApiParameter.PATH
            ),
            OpenApiParameter(name="id", type=OpenApiTypes.STR, location=OpenApiParameter.PATH),
        ],
        request=None,
        responses={
            200: CityOutputSerializer,
            404: OpenApiResponse(description="Not found"),
        },
        summary="Get city's details by admin",
    )
    def retrieve(self, request, country_pk, pk):  # pylint:disable=unused-argument
        """Get city's details."""
        city = CityService.retrieve(actor=request.user, city_id=pk)
        output_serializer = CityOutputSerializer(city)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="country_id", type=OpenApiTypes.STR, location=OpenApiParameter.PATH
            ),
            OpenApiParameter(name="id", type=OpenApiTypes.STR, location=OpenApiParameter.PATH),
        ],
        request=CityUpdateInputSerializer,
        responses={
            200: CityOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Edit city's details by admin",
    )
    def update(self, request, country_pk, pk):  # pylint:disable=unused-argument
        """Update a city's details."""
        incoming_data = CityUpdateInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        city = CityService.update(actor=request.user, city_id=pk, **incoming_data.validated_data)
        output_serializer = CityOutputSerializer(city)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="country_id", type=OpenApiTypes.STR, location=OpenApiParameter.PATH
            ),
            OpenApiParameter(
                name="city_id", type=OpenApiTypes.STR, location=OpenApiParameter.PATH
            ),
        ],
        request=None,
        responses={
            200: CityListPaginatedOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="List all available cities in a country by admin",
    )
    def list(self, request, country_pk):
        """List all cities in a country."""
        cities = CityService.get_paginated_list(
            actor=request.user, country_id=country_pk, query_params=request.query_params
        )
        output_serializer = CityListPaginatedOutputSerializer(cities)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="country_id", type=OpenApiTypes.STR, location=OpenApiParameter.PATH
            ),
            OpenApiParameter(name="id", type=OpenApiTypes.STR, location=OpenApiParameter.PATH),
        ],
        request=None,
        responses={
            204: None,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Delete a city from the DB by admin",
    )
    def destroy(self, request, country_pk, pk):  # pylint:disable=unused-argument
        """Delete a city."""
        incoming_data = CityUpdateInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        CityService.delete(actor=request.user, city_id=pk)
        return Response(status=HTTP_204_NO_CONTENT)
