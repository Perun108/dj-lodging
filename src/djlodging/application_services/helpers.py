from django.core.exceptions import PermissionDenied

from djlodging.domain.users.models import User


def check_staff_permissions(actor: User) -> None:
    if not actor.is_staff:
        raise PermissionDenied


def check_partner_permissions(actor: User) -> None:
    if not actor.is_partner:
        raise PermissionDenied
