import json

from django import http
from django.contrib.auth.views import login
from django.views import View
from django_redis import get_redis_connection
from pymysql import DatabaseError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.users.models import User
from apps.users.serializers import UserInfoSerializer


class UserRegister(View):
    def post(self, request):
        json_dict = json.loads(request.body.decode())
        phonecode = json_dict.get('phonecode')
        mobile = json_dict.get('mobile')
        password = json_dict.get('password')

        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None:
            return http.HttpResponseForbidden('短信验证码无效')
        if phonecode != sms_code_server.decode():
            return http.HttpResponseForbidden('短信验证码有误')
        try:
            user = User.objects.create_user(username=mobile,password=password, mobile=mobile)
        except DatabaseError:
            return http.HttpResponseForbidden('保存信息失败')
        login(request, user)
        return http.JsonResponse({
            "errno": "0",
            "errmsg": "注册成功"
        })
