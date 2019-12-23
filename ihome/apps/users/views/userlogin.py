import json

from apps.users.models import User
from apps.users.serializers import UserInfoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class UserLogin(APIView):
    def post(self,request):
        json_dict = json.loads(request.body.decode())
        serializers = UserInfoSerializer(data=json_dict)
        serializers.is_valid()
        return Response(serializers.data)


