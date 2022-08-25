from django.contrib import admin

from djlodging.domain.bookings.models import Booking

# class BookingAdmin(admin.ModelAdmin):
#     list_display = [
#         "id",
#         "email",
#         "first_name",
#     ]


admin.site.register(Booking)
