from django.urls import include, path
from rest_framework_nested import routers

from djlodging.api.bookings.views import BookingViewSet
from djlodging.api.lodging.views import (
    CityViewSet,
    CountryViewSet,
    LodgingViewSet,
    ReviewViewSet,
)
from djlodging.api.users.views import UserViewSet

router = routers.SimpleRouter()

router.register(r"users", UserViewSet, basename="users")
router.register(r"countries", CountryViewSet, basename="countries")
router.register(r"cities", CityViewSet, basename="cities")
router.register(r"lodgings", LodgingViewSet, basename="lodgings")
router.register(r"bookings", BookingViewSet, basename="bookings")

reviews_router = routers.NestedSimpleRouter(router, r"lodgings", lookup="lodging")
reviews_router.register(r"reviews", ReviewViewSet, basename="reviews")
urlpatterns = [
    path("", include(router.urls)),
    path("", include(reviews_router.urls)),
]
# print(router.urls)
