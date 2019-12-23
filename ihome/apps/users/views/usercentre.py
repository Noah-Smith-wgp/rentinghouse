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


class UserCenter(APIView):
    def get(self, request):
        user = request.user
        user_list = User.objects.get(id=user.id)
        data = User.to_basic_dict(user_list)
        return Response({'errmsg': 'OK', 'errno': '0', 'data': data})


class UserImage(View):
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
            User.objects.filter(username=str(username)).update(avatar=url)
        else:
            print(info)
        data = {
            "avatar_url": settings.QINIU_URL + url
        }
        return JsonResponse({"data": data, "errno": "0", "errmsg": "头像上传成功"})
