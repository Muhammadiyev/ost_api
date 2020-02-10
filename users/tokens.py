import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# nexus Stuff
# from nexus.base import exceptions as exc
from django.utils.translation import ugettext_lazy as _

def get_token_for_user(user, scope):
    """
    Generate a new signed token containing
    a specified user limited for a scope (identified as a string).
    """
    data = {
        "user_%s_id" % (scope): str(user.id),
    }
    return jwt.encode(data, settings.SECRET_KEY).decode()

class BadRequest(BaseException):
    """Exception used on bad arguments detected on api view.
    """
    default_detail = _('Wrong arguments.')


class RequestValidationError(BadRequest):
    default_detail = _('Data validation error')

def get_user_for_password_reset_token(token):
    default_error_messages = {
        'invalid_token': 'Invalid token or the token has expired',
        'user_not_found': 'No user exists for given token'
    }
    try:
        uidb64, reset_token = token.split("::")
    except ValueError:
        raise exc.RequestValidationError(default_error_messages['invalid_token'])

    user_id = decode_uuid_from_base64(uidb64)
    if not user_id:
        raise exc.RequestValidationError(default_error_messages['invalid_token'])

    user = get_user_model().objects.filter(id=user_id).first()

    if not user:
        raise exc.RequestValidationError(default_error_messages['user_not_found'])

    if not PasswordResetTokenGenerator().check_token(user, reset_token):
        raise exc.RequestValidationError(default_error_messages['invalid_token'])

    return user