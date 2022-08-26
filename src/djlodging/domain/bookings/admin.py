from django.contrib import admin

from djlodging.domain.bookings.models import Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "lodging", "date_from", "date_to", "status"]


admin.site.register(Booking, BookingAdmin)
