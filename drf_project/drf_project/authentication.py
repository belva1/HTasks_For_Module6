from rest_framework.authentication import TokenAuthentication
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from rest_framework import exceptions


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
        """
        token.created - token creation time.
        timezone.now() - timezone.timedelta(minutes=10) - current time minus 10 minutes.
        If the token creation time is less than the current time minus 10 minutes, this means 
        that the token was created more than 10 minutes ago.
        """
        if token.created < timezone.now() - timezone.timedelta(minutes=10):
            token.delete()
            raise exceptions.AuthenticationFailed(_('Token has expired.'))

        return (token.user, token)
