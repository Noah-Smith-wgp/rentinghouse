import json
from django.conf import settings
from django.http import *
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
import logging

from apps.users.models import User
from utils.qiniu import qiniu_upload

log = logging.getLogger('django')


# 展示个人中心
class UserCenterView(APIView):
    def get(self, request):
        user = request.user
        user_list = User.objects.get(id=user.id)
        data = User.to_basic_dict(user_list)
        return Response({'errmsg': 'OK', 'errno': '0', 'data': data})


# 上传头像
class UserImageView(View):
    def post(self, request):
        avatar = request.FILES.get('avatar').read()
        username = request.user

        url = qiniu_upload(avatar)
        try:
            User.objects.filter(username=str(username)).update(avatar=url)
        except Exception as e:
            log.error(e)

        data = {
            "avatar_url": settings.QINIU_URL + url
        }
        return JsonResponse({"data": data, "errno": "0", "errmsg": "头像上传成功"})


# 用户名修改
class UserNameView(View):
    def put(self, request):
        name = json.loads(request.body.decode())
        username = request.user
        try:
            User.objects.filter(username=str(username)).update(username=name.get("name"))
        except Exception as e:
            log.error(e)
        return JsonResponse({"errno": "0", "errmsg": "修改成功"})


# 实名认证
class UserAuthView(View):
    # 获取认证信息
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
