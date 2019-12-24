import json
import random

import qiniu
from django.conf import settings
from django.http import *
from django.views import View
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView

from apps.users.models import User
from apps.users.serializers import UserInfoSerializer
import logging

log = logging.getLogger('django')


class UserCenterView(APIView):
    def get(self, request):
        user = request.user
        user_list = User.objects.get(id=user.id)
        data = User.to_basic_dict(user_list)
        return Response({'errmsg': 'OK', 'errno': '0', 'data': data})


class UserImageView(View):
    def post(self, request):
        avatar = request.FILES.get('avatar').read()
        username = request.user
        q = qiniu.Auth(access_key=settings.ACCESS_KEY, secret_key=settings.SECRET_KEYS)
        num = '%06d' % random.randint(0, 999999)
        key = str(username) + str(num)
        token = q.upload_token(bucket=settings.BUCKET_NAME)
        ret, info = qiniu.put_data(token, key, avatar)
        url = ret.get('key')
        if ret is not None:
            print('All is OK')
            try:
                User.objects.filter(username=str(username)).update(avatar=url)
            except Exception as e:
                log.error(e)
        else:
            print(info)
        data = {
            "avatar_url": settings.QINIU_URL + url
        }
        return JsonResponse({"data": data, "errno": "0", "errmsg": "头像上传成功"})


class UserNameView(View):
    def put(self, request):
        name = json.loads(request.body.decode())
        username = request.user
        try:
            User.objects.filter(username=str(username)).update(username=name.get("name"))
        except Exception as e:
            log.error(e)
        return JsonResponse({"errno": "0", "errmsg": "修改成功"})


class UserAuthView(View):

    def get(self, request):
        user = request.user
        try:
            user = User.objects.get(username=user.username)
        except Exception as e:
            log.error(e)
        data = User.to_auth_dict(user)
        return JsonResponse({"errno": "0", "errmsg": "OK", "data": data})

    def post(self, request):
        data = json.loads(request.body.decode())
        real_name = data.get('real_name')
        id_card = data.get('id_card')
        user = request.user
        try:
            User.objects.filter(username=user.username).update(id_card=id_card, real_name=real_name)
        except Exception as e:
            log.error(e)
        return JsonResponse({"errno": "0", "errmsg": "认证信息保存成功"})
