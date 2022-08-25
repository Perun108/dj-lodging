from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.viewsets import ViewSet

from djlodging.api.helpers import validate_required_query_params_with_any
from djlodging.api.lodging.serializers import (
    AvailableLodgingListInputSerializer,
    AvailableLodgingListOutputSerializer,
    CityCreateInputSerializer,
    CityCreateOutputSerializer,
    CountryCreateInputSerializer,
    CountryCreateOutputSerializer,
    LodgingCreateInputSerializer,
    LodgingOutputSerializer,
)
from djlodging.api.permissions import IsPartner
from djlodging.application_services.lodgings import (
    CityService,
    CountryService,
    LodgingService,
)
from djlodging.domain.lodgings.repositories import LodgingRepository


class CountryViewSet(ViewSet):
    permission_classes = (IsAdminUser,)

    def create(self, request):
        incoming_data = CountryCreateInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        country = CountryService.create(actor=request.user, **incoming_data.validated_data)
        output_serializer = CountryCreateOutputSerializer(country)
        return Response(data=output_serializer.data, status=HTTP_201_CREATED)


class CityViewSet(ViewSet):
    permission_classes = (IsAdminUser,)

    def create(self, request):
        incoming_data = CityCreateInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)
        city = CityService.create(actor=request.user, **incoming_data.validated_data)
        output_serializer = CityCreateOutputSerializer(city)
        return Response(data=output_serializer.data, status=HTTP_201_CREATED)


class LodgingViewSet(ViewSet):
    def get_permissions(self):
        if self.action in ["list", "retrieve", "list_available"]:
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsPartner,)
        return super().get_permissions()

    def create(self, request):
        input_serializer = LodgingCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        lodging = LodgingService.create(actor=request.user, **input_serializer.validated_data)
        output_serializer = LodgingOutputSerializer(lodging)
        return Response(data=output_serializer.data, status=HTTP_201_CREATED)

    @action(detail=False, url_path="available")
    def list_available(self, request):
        validate_required_query_params_with_any(
            required_params=["country", "city"],
            query_params=request.query_params,
        )
        input_serializer = AvailableLodgingListInputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)
        available_lodging = LodgingRepository.get_available_at_destination_for_dates(
            **input_serializer.validated_data
        )
        output_serializer = AvailableLodgingListOutputSerializer(available_lodging, many=True)
        return Response(data=output_serializer.data, status=HTTP_200_OK)
