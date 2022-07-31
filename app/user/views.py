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
