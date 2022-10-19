from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ViewSet

from djlodging.api.lodging.serializers import (
    ReviewCreateInputSerializer,
    ReviewOutputSerializer,
    ReviewUpdateInputSerializer,
)
from djlodging.application_services.lodgings import ReviewService
from djlodging.domain.lodgings.repositories import ReviewRepository


class ReviewViewSet(ViewSet):
    @extend_schema(
        parameters=[
            OpenApiParameter("lodging_id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH)
        ],
        request=ReviewCreateInputSerializer,
        responses={
            201: ReviewOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def create(self, request, lodging_pk):
        input_serializer = ReviewCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        review = ReviewService.create(
            lodging_id=lodging_pk, user=request.user, **input_serializer.validated_data
        )
        output_serializer = ReviewOutputSerializer(review)
        return Response(output_serializer.data, status=HTTP_201_CREATED)

    @extend_schema(
        parameters=[
            OpenApiParameter("lodging_id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH)
        ],
        request=None,
        responses={
            200: ReviewOutputSerializer(many=True),
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def list(self, request, lodging_pk):
        reviews = ReviewRepository.get_list(lodging_id=lodging_pk)
        output_serializer = ReviewOutputSerializer(reviews, many=True)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("lodging_id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
            OpenApiParameter("review_id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
        ],
        request=None,
        responses={
            200: ReviewOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def retrieve(self, request, lodging_pk, pk):
        review = ReviewRepository.get_by_id(review_id=pk)
        output_serializer = ReviewOutputSerializer(review)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("lodging_id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
            OpenApiParameter("review_id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
        ],
        request=ReviewUpdateInputSerializer,
        responses={
            200: ReviewOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def update(self, request, lodging_pk, pk):
        input_serializer = ReviewUpdateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        review = ReviewService.update(
            actor=request.user, review_id=pk, **input_serializer.validated_data
        )
        output_serializer = ReviewOutputSerializer(review)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("lodging_id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
            OpenApiParameter("review_id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
        ],
        request=None,
        responses={
            204: None,
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def destroy(self, request, lodging_pk, pk):
        ReviewService.delete(actor=request.user, review_id=pk)
        return Response(status=HTTP_204_NO_CONTENT)
