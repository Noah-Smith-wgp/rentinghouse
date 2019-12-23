from django.http import *
from django.views import View
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView

from apps.users.models import User
from apps.users.serializers import UserInfoSerializer


class UserCenter(APIView):
    def get(self, request):
        user = request.user
        user_list = User.objects.get(id=user.id)
        rst_dict = {
            # "avatar": user_list.avatar,
            # "create_time": user_list.create_time,
            "mobile": user_list.mobile,
            "name": user_list.username,
            "user_id": user_list.id
        }
        return Response({'errmsg': 'OK', 'errno': '0', 'data': rst_dict})