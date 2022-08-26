from django.urls import include, path
from rest_framework import routers

from djlodging.api.bookings.views import BookingViewSet
from djlodging.api.lodging.views import CityViewSet, CountryViewSet, LodgingViewSet
from djlodging.api.payments.views import PaymentViewSet
from djlodging.api.users.views import UserViewSet

router = routers.SimpleRouter()

router.register(r"users", UserViewSet, basename="user")
router.register(r"countries", CountryViewSet, basename="country")
router.register(r"cities", CityViewSet, basename="city")
router.register(r"lodgings", LodgingViewSet, basename="lodging")
router.register(r"bookings", BookingViewSet, basename="booking")
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
]
# print(router.urls)
