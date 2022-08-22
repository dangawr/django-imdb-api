from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView


@api_view(['POST'])
def logout_view(request):
    """View for logout user."""
    if request.method == 'POST':
        request.user.auth_token.delete()

        return Response(status=status.HTTP_200_OK)


class RegisterUserApiView(CreateAPIView):
    """View for user registration."""
    serializer_class = UserSerializer


from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="IMDB Clone"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )