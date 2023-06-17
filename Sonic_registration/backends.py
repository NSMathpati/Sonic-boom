#Creating Custon Email Backend to authenticate with email instead of username
# Path: Sonic_registration\backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
import pdb


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Check if user exists in the database
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            return None
        else:
            # Check if the password is valid for the user we found
            if user.check_password(password):
                return user
        return None