from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .models import UM
from .serializers import UMSerializer


@api_view(['GET'])
def user_detail(request):
    cur_user = request.user
    serializer = UMSerializer(cur_user)
    obj = {
        "id": serializer.data['id'],
        "username": serializer.data['username'],
    }
    return Response(obj)