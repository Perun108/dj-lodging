from django.urls import include, path
from rest_framework_nested import routers

from djlodging.api.bookings.views import BookingViewSet, MyBookingViewSet
from djlodging.api.lodging.views import (
    CityViewSet,
    CountryViewSet,
    LodgingViewSet,
    MyReviewViewSet,
    ReviewViewSet,
)
from djlodging.api.users.views import MeViewSet, UserViewSet

router = routers.SimpleRouter()

router.register(r"users/me/bookings", MyBookingViewSet, basename="my-bookings")
router.register(r"users/me/reviews", MyReviewViewSet, basename="my-reviews")
router.register(r"users", MeViewSet, basename="me")
router.register(r"users", UserViewSet, basename="users")
router.register(r"countries", CountryViewSet, basename="countries")
router.register(r"lodgings", LodgingViewSet, basename="lodgings")
router.register(r"bookings", BookingViewSet, basename="bookings")

cities_router = routers.NestedSimpleRouter(router, r"countries", lookup="country")
cities_router.register(r"cities", CityViewSet, basename="cities")

reviews_router = routers.NestedSimpleRouter(router, r"lodgings", lookup="lodging")
reviews_router.register(r"reviews", ReviewViewSet, basename="reviews")

urlpatterns = [
    path("users/", include("djlodging.api.users.urls")),
    path("", include(router.urls)),
    path("", include(cities_router.urls)),
    path("", include(reviews_router.urls)),
]
# print(reviews_router.urls)
# print("\n")
# print(router.urls)
