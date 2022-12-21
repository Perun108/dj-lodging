"""API module for the management of Reviews."""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ViewSet

from djlodging.api.lodging.serializers import (
    MyReviewOutputSerializer,
    MyReviewsPaginatedListOutputSerializer,
    ReviewCreateInputSerializer,
    ReviewOutputSerializer,
    ReviewPaginatedListOutputSerializer,
    ReviewUpdateInputSerializer,
)
from djlodging.application_services.lodgings import ReviewService
from djlodging.domain.lodgings.repositories import ReviewRepository


class ReviewViewSet(ViewSet):
    """ViewSet for the management of Reviews by admin."""

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
        """List all reviews for a lodging."""
        reviews = ReviewRepository.get_paginated_list_by_lodging(
            lodging_id=lodging_pk, query_params=request.query_params
        )
        output_serializer = ReviewPaginatedListOutputSerializer(reviews)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("lodging_id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
            OpenApiParameter("id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
        ],
        request=None,
        responses={
            200: ReviewOutputSerializer,
            404: OpenApiResponse(description="Not found"),
        },
        summary="Get a review's details by any user",
    )
    def retrieve(self, request, lodging_pk, pk):  # pylint:disable=unused-argument
        """Get a review's details."""
        review = ReviewRepository.get_by_id(review_id=pk)
        output_serializer = ReviewOutputSerializer(review)
        return Response(output_serializer.data, status=HTTP_200_OK)


class MyReviewViewSet(ViewSet):
    """ViewSet for the management of Reviews by their users."""

    @extend_schema(
        request=ReviewCreateInputSerializer,
        responses={
            201: ReviewOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Add a review for lodging",
    )
    def create(self, request):
        """Create new review for a lodging."""
        input_serializer = ReviewCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        review = ReviewService.create(user=request.user, **input_serializer.validated_data)
        output_serializer = ReviewOutputSerializer(review)
        return Response(output_serializer.data, status=HTTP_201_CREATED)

    @extend_schema(
        request=None,
        responses={
            200: MyReviewsPaginatedListOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="List my reviews for all my booked lodgings",
    )
    def list(self, request):
        """List all reviews by a logged in user."""
        my_reviews = ReviewRepository.get_paginated_list_by_user(
            user=request.user, query_params=request.query_params
        )
        output_serializer = MyReviewsPaginatedListOutputSerializer(my_reviews)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
        ],
        request=None,
        responses={
            200: MyReviewOutputSerializer,
            404: OpenApiResponse(description="Not found"),
        },
        summary="Get my review's details",
    )
    def retrieve(self, request, pk):
        """Get a user's review's details."""
        review = ReviewService.retrieve_my(actor=request.user, review_id=pk)
        output_serializer = MyReviewOutputSerializer(review)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
        ],
        request=ReviewUpdateInputSerializer,
        responses={
            200: ReviewOutputSerializer,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Edit my review",
    )
    def update(self, request, pk):
        """Update a review by its author."""
        input_serializer = ReviewUpdateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        review = ReviewService.update(
            actor=request.user, review_id=pk, **input_serializer.validated_data
        )
        output_serializer = ReviewOutputSerializer(review)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter("id", type=OpenApiTypes.UUID, location=OpenApiParameter.PATH),
        ],
        request=None,
        responses={
            204: None,
            400: OpenApiResponse(description="Bad request"),
        },
        summary="Delete my review",
    )
    def destroy(self, request, pk):
        """Delete a review by its author."""
        ReviewService.delete(actor=request.user, review_id=pk)
        return Response(status=HTTP_204_NO_CONTENT)
