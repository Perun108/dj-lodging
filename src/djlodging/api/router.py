from django.urls import include, path
from rest_framework import routers

from djlodging.api.lodging.views import CityViewSet, CountryViewSet, LodgingViewSet
from djlodging.api.users.views import UserViewSet

router = routers.SimpleRouter()

router.register(r"users", UserViewSet, basename="user")
router.register(r"countries", CountryViewSet, basename="country")
router.register(r"cities", CityViewSet, basename="city")
router.register(r"lodgings", LodgingViewSet, basename="lodging")

urlpatterns = [
    path("", include(router.urls)),
]
