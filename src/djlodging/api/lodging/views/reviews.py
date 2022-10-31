from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ViewSet

from djlodging.api.lodging.serializers import (
    MyReviewsListOutputSerializer,
    ReviewCreateInputSerializer,
    ReviewOutputSerializer,
    ReviewPaginatedListOutputSerializer,
    ReviewUpdateInputSerializer,
)
from djlodging.api.pagination import paginate_queryset
from djlodging.application_services.lodgings import ReviewService
from djlodging.domain.lodgings.repositories import ReviewRepository


class ReviewViewSet(ViewSet):
    @extend_schema(
        parameters=[
            OpenApiParameter("lodging_id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH)
        ],
        request=None,
        responses={
            200: ReviewPaginatedListOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="List all lodging's reviews by any user",
    )
    def list(self, request, lodging_pk):
        reviews = ReviewRepository.get_list(lodging_id=lodging_pk)
        qs = paginate_queryset(reviews, request.query_params)
        output_serializer = ReviewPaginatedListOutputSerializer(qs)
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
        summary="Get a review's details by any user",
    )
    def retrieve(self, request, lodging_pk, pk):
        review = ReviewRepository.get_by_id(review_id=pk)
        output_serializer = ReviewOutputSerializer(review)
        return Response(output_serializer.data, status=HTTP_200_OK)


class MyReviewViewSet(ViewSet):
    @extend_schema(
        request=ReviewCreateInputSerializer,
        responses={
            201: ReviewOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Add a review for lodging",
    )
    def create(self, request):
        input_serializer = ReviewCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        review = ReviewService.create(user=request.user, **input_serializer.validated_data)
        output_serializer = ReviewOutputSerializer(review)
        return Response(output_serializer.data, status=HTTP_201_CREATED)

    @extend_schema(
        request=None,
        responses={
            200: MyReviewsListOutputSerializer(many=True),
            400: OpenApiResponse(description="Bad request"),
        },
        summary="List my reviews for all my booked lodgings",
    )
    def list(self, request):
        my_reviews = ReviewRepository.get_my_list(user=request.user)
        output_serializer = MyReviewsListOutputSerializer(my_reviews, many=True)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("review_id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
        ],
        request=None,
        responses={
            200: MyReviewsListOutputSerializer(many=True),
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Get my review's details",
    )
    def retrieve(self, request, pk):
        review = ReviewService.retrieve_my(actor=request.user, review_id=pk)
        output_serializer = MyReviewsListOutputSerializer(review)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("review_id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
        ],
        request=ReviewUpdateInputSerializer,
        responses={
            200: ReviewOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Edit my review",
    )
    def update(self, request, pk):
        input_serializer = ReviewUpdateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        review = ReviewService.update(
            actor=request.user, review_id=pk, **input_serializer.validated_data
        )
        output_serializer = ReviewOutputSerializer(review)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("review_id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
        ],
        request=None,
        responses={
            204: None,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Delete my review",
    )
    def destroy(self, request, pk):
        ReviewService.delete(actor=request.user, review_id=pk)
        return Response(status=HTTP_204_NO_CONTENT)
