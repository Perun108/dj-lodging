from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ViewSet

from djlodging.api.lodging.serializers import (
    CityCreateInputSerializer,
    CityOutputSerializer,
    CityUpdateInputSerializer,
)
from djlodging.application_services.lodgings import CityService


class CityViewSet(ViewSet):
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
    )
    def create(self, request, country_pk):
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
            OpenApiParameter(
                name="city_id", type=OpenApiTypes.STR, location=OpenApiParameter.PATH
            ),
        ],
        request=None,
        responses={
            200: CityOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def retrieve(self, request, country_pk, pk):
        city = CityService.retrieve(actor=request.user, city_id=pk)
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
        request=CityUpdateInputSerializer,
        responses={
            200: CityOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def update(self, request, country_pk, pk):
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
            200: CityOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def list(self, request, country_pk):
        cities = CityService.get_list(actor=request.user, country_id=country_pk)
        output_serializer = CityOutputSerializer(cities, many=True)
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
            204: None,
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def destroy(self, request, country_pk, pk):
        incoming_data = CityUpdateInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        CityService.delete(actor=request.user, city_id=pk)
        return Response(status=HTTP_204_NO_CONTENT)
