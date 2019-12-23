import json

from django import http
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View

from apps.users.models import User
from apps.users.serializers import UserInfoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

'''
// 已登录：
{
    "errno": "0",
    "errmsg": "已登录",
    "data": {
        "name": "用户名"
    }
}
// 未登录：
{
    "errno": "4101",
    "errmsg": "未登录"
}
'''


class UserLogin(View):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return http.JsonResponse({"errno": "4101", "errmsg": "未登录"})
        data = {
            "user_id": user.id,
            "name": user.username
        }
        return http.JsonResponse({"errno": "0", "errmsg": "已登录", "data": data})

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
        login(request, user)
        return http.JsonResponse({
            "errno": "0",
            "errmsg": "登录成功",
            "data": {
                "name": user.username
            }
        })

    def delete(self, request):
        logout(request)
        return http.JsonResponse({"errno": "0", "errmsg": "已登出"})
