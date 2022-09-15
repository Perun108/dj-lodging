from django.contrib import admin

from djlodging.domain.lodgings.models import (
    City,
    Country,
    Lodging,
    LodgingImage,
    Review,
)


class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]


class CityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "country", "region"]


class LodgingAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "city", "type", "number_of_rooms", "price"]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "lodging", "score"]


admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Lodging, LodgingAdmin)
admin.site.register(LodgingImage)
admin.site.register(Review, ReviewAdmin)
