from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# from .models import UM
from .serializers import UMSerializer


class UserDetail(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            serializer = UMSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)