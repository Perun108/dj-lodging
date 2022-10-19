from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ViewSet

from djlodging.api.lodging.serializers import (
    CountryCreateInputSerializer,
    CountryOutputSerializer,
    CountryUpdateInputSerializer,
)
from djlodging.application_services.lodgings import CountryService


class CountryViewSet(ViewSet):
    permission_classes = (IsAdminUser,)

    @extend_schema(
        request=CountryCreateInputSerializer,
        responses={
            201: CountryOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def create(self, request):
        incoming_data = CountryCreateInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        country = CountryService.create(actor=request.user, **incoming_data.validated_data)
        output_serializer = CountryOutputSerializer(country)
        return Response(data=output_serializer.data, status=HTTP_201_CREATED)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="country_id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        request=None,
        responses={
            200: CountryOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def retrieve(self, request, pk):
        country = CountryService.retrieve(actor=request.user, country_id=pk)
        output_serializer = CountryOutputSerializer(country)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        request=None,
        responses={
            200: CountryOutputSerializer(many=True),
        },
    )
    def list(self, request):
        countries = CountryService.get_list(actor=request.user)
        output_serializer = CountryOutputSerializer(countries, many=True)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="country_id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        request=CountryUpdateInputSerializer,
        responses={
            200: CountryOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def update(self, request, pk):
        incoming_data = CountryUpdateInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        country = CountryService.update(
            actor=request.user, country_id=pk, **incoming_data.validated_data
        )
        output_serializer = CountryOutputSerializer(country)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="country_id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        request=None,
        responses={
            204: None,
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def destroy(self, request, pk):
        CountryService.delete(actor=request.user, country_id=pk)
        return Response(status=HTTP_204_NO_CONTENT)