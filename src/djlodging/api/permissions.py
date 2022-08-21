from rest_framework.permissions import BasePermission


class IsPartner(BasePermission):
    """
    Allows access only to partner users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_partner)
