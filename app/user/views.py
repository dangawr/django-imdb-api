from rest_framework.decorators import api_view
from .serializers import UserSerializer
from rest_framework.response import Response

# Create your views here.


@api_view(['POST'])
def register_view(request):

    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
