from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.viewsets import ViewSet

from djlodging.api.helpers import validate_required_query_params_with_any
from djlodging.api.lodging.serializers import (
    LodgingCreateInputSerializer,
    LodgingCreateOutputSerializer,
    LodgingListInputSerializer,
    LodgingListOutputSerializer,
    LodgingOutputSerializer,
    MyReviewsListOutputSerializer,
)
from djlodging.api.permissions import IsPartner
from djlodging.application_services.lodgings import LodgingService
from djlodging.domain.lodgings.repositories import LodgingRepository, ReviewRepository


class LodgingViewSet(ViewSet):
    def get_permissions(self):
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
    )
    def create(self, request):
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
        request=LodgingListInputSerializer,
        responses={
            200: LodgingListOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def list(self, request):
        validate_required_query_params_with_any(
            required_params=["country", "city"],
            query_params=request.query_params,
        )
        input_serializer = LodgingListInputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)
        lodgings = LodgingRepository.get_list(**input_serializer.validated_data)
        output_serializer = LodgingListOutputSerializer(lodgings, many=True)
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
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def retrieve(self, request, pk):
        lodging = LodgingRepository.retrieve_lodging_with_average_rating(pk)
        output_serializer = LodgingOutputSerializer(lodging)
        return Response(data=output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("lodging_id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH)
        ],
        request=None,
        responses={
            200: MyReviewsListOutputSerializer(many=True),
            400: OpenApiResponse(description="Bad request"),
        },
    )
    @action(detail=False, methods=["get"], url_path="my-reviews")
    def my_reviews(self, request):
        """
        This method must be here and not in the ReviewViewSet where it may seem to belong
        because there shouldn't be {lodging_id} in the URL path ('my reviews' is for ALL lodgings).
        """
        my_reviews = ReviewRepository.get_my_list(user=request.user)
        output_serializer = MyReviewsListOutputSerializer(my_reviews, many=True)
        return Response(output_serializer.data, status=HTTP_200_OK)
