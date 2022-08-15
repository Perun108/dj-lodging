from django.contrib import admin
from django.contrib.auth.models import Group

from djbooking.domain.users.models import ConfirmationCode, User


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "email",
        "first_name",
    ]


# class ConfirmationCodeAdmin(admin.ModelAdmin):
#     list_display = [
#         "id",
#         "email",
#         "first_name",
#     ]


admin.site.register(User, UserAdmin)
admin.site.register(ConfirmationCode)
admin.site.unregister(Group)
