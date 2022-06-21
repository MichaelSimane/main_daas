from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from .models import DAAS_User
from django.db.models import Q
class AuthBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user(self, user_id):
       try:
          return DAAS_User.objects.get(pk=user_id)
       except DAAS_User.DoesNotExist:
          return None

    def authenticate(self, username, password):
        try:
            user = DAAS_User.objects.get(
                Q(username=username) | Q(email=username) | Q(phone=username)
            )
        except DAAS_User.DoesNotExist:
            return None
        return user if user.check_password(password) else None
class CaseInsensitive(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
            user = UserModel._default_manager.get(**{case_insensitive_username_field: username})
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user