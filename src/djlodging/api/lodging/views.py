from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ViewSet

from djlodging.api.helpers import validate_required_query_params_with_any
from djlodging.api.lodging.serializers import (
    CityCreateInputSerializer,
    CityOutputSerializer,
    CityUpdateInputSerializer,
    CountryCreateInputSerializer,
    CountryOutputSerializer,
    CountryUpdateInputSerializer,
    LodgingCreateInputSerializer,
    LodgingCreateOutputSerializer,
    LodgingListInputSerializer,
    LodgingListOutputSerializer,
    LodgingOutputSerializer,
    ReviewCreateInputSerializer,
    ReviewOutputSerializer,
)
from djlodging.api.permissions import IsPartner
from djlodging.application_services.lodgings import (
    CityService,
    CountryService,
    LodgingService,
    ReviewService,
)
from djlodging.domain.lodgings.repositories import LodgingRepository, ReviewRepository


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
