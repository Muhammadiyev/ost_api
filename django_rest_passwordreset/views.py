from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from rest_framework import status, serializers, exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from django_rest_passwordreset.serializers import EmailSerializer, PasswordTokenSerializer, TokenSerializer
from django_rest_passwordreset.models import ResetPasswordToken, clear_expired, get_password_reset_token_expiry_time, \
    get_password_reset_lookup_field
from django_rest_passwordreset.signals import reset_password_token_created, pre_password_reset, post_password_reset

User = get_user_model()

__all__ = [
    'ValidateToken',
    'ResetPasswordConfirm',
    'ResetPasswordRequestToken',
    'reset_password_validate_token',
    'reset_password_confirm',
    'reset_password_request_token'
]

HTTP_USER_AGENT_HEADER = getattr(
    settings, 'DJANGO_REST_PASSWORDRESET_HTTP_USER_AGENT_HEADER', 'HTTP_USER_AGENT')
HTTP_IP_ADDRESS_HEADER = getattr(
    settings, 'DJANGO_REST_PASSWORDRESET_IP_ADDRESS_HEADER', 'REMOTE_ADDR')


class ResetPasswordValidateToken(GenericAPIView):

    throttle_classes = ()
    permission_classes = ()
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        reset_password_token = ResetPasswordToken.objects.filter(
            key=token).first()

        if reset_password_token is None:
            return Response({'status': 'notfound'}, status=status.HTTP_404_NOT_FOUND)

        expiry_date = reset_password_token.created_at + \
            timedelta(hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:

            reset_password_token.delete()
            return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'status': 'OK'})


class ResetPasswordConfirm(GenericAPIView):

    throttle_classes = ()
    permission_classes = ()
    serializer_class = PasswordTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        token = serializer.validated_data['token']

        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        reset_password_token = ResetPasswordToken.objects.filter(
            key=token).first()

        if reset_password_token is None:
            return Response({'status': 'notfound'}, status=status.HTTP_404_NOT_FOUND)

        expiry_date = reset_password_token.created_at + \
            timedelta(hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            reset_password_token.delete()
            return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)

        if reset_password_token.user.eligible_for_reset():
            pre_password_reset.send(
                sender=self.__class__, user=reset_password_token.user)
            try:
                validate_password(
                    password,
                    user=reset_password_token.user,
                    password_validators=get_password_validators(
                        settings.AUTH_PASSWORD_VALIDATORS)
                )
            except ValidationError as e:
                raise exceptions.ValidationError({
                    'password': e.messages
                })

            reset_password_token.user.set_password(password)
            reset_password_token.user.save()
            post_password_reset.send(
                sender=self.__class__, user=reset_password_token.user)

        ResetPasswordToken.objects.filter(
            user=reset_password_token.user).delete()

        return Response({'status': 'OK'})


class ResetPasswordRequestToken(GenericAPIView):

    throttle_classes = ()
    permission_classes = ()
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        now_minus_expiry_time = timezone.now(
        ) - timedelta(hours=password_reset_token_validation_time)

        clear_expired(now_minus_expiry_time)

        users = User.objects.filter(
            **{'{}__iexact'.format(get_password_reset_lookup_field()): email})

        active_user_found = False

        for user in users:
            if user.eligible_for_reset():
                active_user_found = True

        if not active_user_found and not getattr(settings, 'DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE', False):
            raise exceptions.ValidationError({
                'email': [_(
                    "There is no active user associated with this e-mail address or the password can not be changed")],
            })

        for user in users:
            if user.eligible_for_reset():
                token = None

                if user.password_reset_tokens.all().count() > 0:
                    token = user.password_reset_tokens.all()[0]
                else:
                    token = ResetPasswordToken.objects.create(
                        user=user,
                        user_agent=request.META.get(
                            HTTP_USER_AGENT_HEADER, ''),
                        ip_address=request.META.get(
                            HTTP_IP_ADDRESS_HEADER, ''),
                    )

                reset_password_token_created.send(
                    sender=self.__class__, instance=self, reset_password_token=token)
        return Response({'status': 'OK'})


reset_password_validate_token = ResetPasswordValidateToken.as_view()
reset_password_confirm = ResetPasswordConfirm.as_view()
reset_password_request_token = ResetPasswordRequestToken.as_view()
