from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from apps.verifications.libs.captcha.captcha import captcha


class UserImagesCode(View):
    def get(self,request):
        cul = request.GET.get('cul')
        # 生成图形验证码
        text, image = captcha.generate_captcha()
        print('图形验证码是:',text)
        # 保存图形验证码
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s' % cul, 3600, text)
        # 响应图形验证码
        return http.HttpResponse(image, content_type='image/jpg')

