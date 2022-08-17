from django.contrib import admin
from django.contrib.auth.models import Group

from djlodging.domain.users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "email",
        "first_name",
    ]


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
