from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.db.models import Q

from apps.account.models import User

UserModel = get_user_model()


class CustomAuthenticationBackend(BaseBackend):
    """
    Authenticate Custom User
    """

    def authenticate(self, request, user_phone=None, password=None, **kwargs):
        if user_phone is None:
            user_phone = kwargs.get(UserModel.USERNAME_FIELD)
        if user_phone is None or password is None:
            return
        try:
            user = User.objects.get(
                Q(email=user_phone) | Q(user_phone=user_phone)
            )
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None
