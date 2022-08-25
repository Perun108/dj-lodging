from django.contrib import admin

from djlodging.domain.lodgings.models import City, Country, Lodging, LodgingImage


class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]


class CityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "country", "region"]


class LodgingAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "city", "type", "number_of_rooms", "price"]


admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Lodging, LodgingAdmin)
admin.site.register(LodgingImage)
