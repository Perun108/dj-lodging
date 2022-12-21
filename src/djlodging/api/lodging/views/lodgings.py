"""API module for the management of Lodgings."""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ViewSet

from djlodging.api.lodging.serializers import (
    LodgingCreateInputSerializer,
    LodgingCreateOutputSerializer,
    LodgingListPaginatedOutputSerializer,
    LodgingOutputSerializer,
    LodgingUpdateInputSerializer,
)
from djlodging.api.permissions import IsPartner
from djlodging.application_services.lodgings import LodgingService
from djlodging.domain.lodgings.repositories import LodgingRepository


class LodgingViewSet(ViewSet):
    """ViewSet for the management of Lodgings."""

    def get_permissions(self):
        """Set respective roles' permissions for ViewSet actions."""
        if self.action in ["list", "retrieve"]:
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsPartner,)
        return super().get_permissions()

    @extend_schema(
        request=LodgingCreateInputSerializer,
        responses={
            201: LodgingCreateOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Add a lodging by partner",
    )
    def create(self, request):
        """Create a new lodging."""
        input_serializer = LodgingCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        lodging = LodgingService.create(actor=request.user, **input_serializer.validated_data)
        output_serializer = LodgingCreateOutputSerializer(lodging)
        return Response(data=output_serializer.data, status=HTTP_201_CREATED)

    @extend_schema(
        description="Filter by country or city. At least one of the two is required",
        parameters=[
            OpenApiParameter(
                name="country",
                description="Filter by country",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="city",
                description="Filter by city",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
        ],
        request=None,
        responses={
            200: LodgingListPaginatedOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="List lodgings in a city available for given dates by any user",
    )
    def list(self, request):
        """List lodgings according to the query_params."""
        lodgings = LodgingRepository.get_paginated_filtered_list(query_params=request.query_params)
        output_serializer = LodgingListPaginatedOutputSerializer(lodgings)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                description="Lodging id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            ),
        ],
        request=None,
        responses={
            200: LodgingOutputSerializer,
            404: OpenApiResponse(description="Not found"),
        },
        summary="Get lodging's details by any user",
    )
    def retrieve(self, request, pk):
        """Get a single lodging's details

        Args:
            request (HttRequest): request from the Frontend
            pk (UUID): lodging's id

        Returns:
            HttpResponse: serialized lodging's details
        """
        lodging = LodgingRepository.retrieve_lodging_with_average_rating(pk)
        output_serializer = LodgingOutputSerializer(lodging)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                description="Lodging id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            ),
        ],
        request=LodgingUpdateInputSerializer,
        responses={
            200: LodgingOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Update lodging's details by its owner",
    )
    def update(self, request, pk):
        """Update a lodging's details."""
        input_serializer = LodgingUpdateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        lodging = LodgingService.update(
            actor=request.user, lodging_id=pk, **input_serializer.validated_data
        )
        output_serializer = LodgingOutputSerializer(lodging)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id",
                description="Lodging id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            ),
        ],
        request=None,
        responses={
            204: None,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Delete lodging by its owner",
    )
    def delete(self, request, pk):
        """Delete a lodging."""
        LodgingService.delete(actor=request.user, lodging_id=pk)
        return Response(status=HTTP_204_NO_CONTENT)
