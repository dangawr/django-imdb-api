from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status


@api_view(['POST'])
def logout_view(request):

    if request.method == 'POST':
        request.user.auth_token.delete()

        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def register_view(request):

    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)

            data['response'] = "Success"
            data['username'] = user.username
            data['email'] = user.email
            data['token'] = token.key

        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)
