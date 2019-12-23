import json

from django import http
from django.contrib.auth import authenticate
from django.contrib.auth.views import login

from apps.users.models import User
from apps.users.serializers import UserInfoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class UserLogin(APIView):
    def post(self, request):
        json_dict = json.loads(request.body.decode())
        serializers = UserInfoSerializer(data=json_dict)
        serializers.is_valid()
        data = serializers.data
        mobile = data.get('mobile')
        password = data.get('password')
        user = authenticate(username=mobile, password=password)
        if user is None:
            return http.HttpResponseForbidden('账号或密码错误')
        return http.JsonResponse({
            "errno": "0",
            "errmsg": "登录成功"
        })

