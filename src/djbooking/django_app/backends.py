from django.contrib.auth import backends, get_user_model
from django.db.models import Q

User = get_user_model()


class EmailOrUsernameModelBackend(backends.ModelBackend):
    # you can't use any other name for 'username' because
    # of JWT TokenObtainSerializer's 'User.USERNAME_FIELD'.
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
