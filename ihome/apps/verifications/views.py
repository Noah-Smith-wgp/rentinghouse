import json
import random
import re
from django import http
from django.views import View
from django_redis import get_redis_connection

from apps.verifications.libs.captcha.captcha import captcha
from apps.verifications.txyun.sms_txy import Sms_txy
# Create your views here.


# 图形验证
class UserImagesCode(View):
    def get(self, request):
        cur = request.GET.get('cur')
        # 生成图形验证码
        text, image = captcha.generate_captcha()
        print('图形验证码是:', text)
        # 保存图形验证码
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s' % cur, 3600, text)
        # 响应图形验证码
        return http.HttpResponse(image, content_type='image/jpg')


# 短信验证
class SmsCode(View):
    def post(self, request):
        data_dict = json.loads(request.body.decode())
        id = data_dict.get('id')
        mobile = data_dict.get('mobile')
        text = data_dict.get('text')
        if not all([id, mobile, text]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        # 创建连接到redis的对象
        redis_conn = get_redis_connection('verify_code')
        # 提取图形验证码
        image_code_server = redis_conn.get('img_%s' % id)
        if image_code_server is None:
            # 图形验证码过期或者不存在
            return http.JsonResponse({'code': 4004, 'errmsg': '图形验证码失效'})
        # 删除图形验证码，避免恶意测试图形验证码
        redis_conn.delete('img_%s' % id)
        # 对比图形验证码
        image_code_server = image_code_server.decode()  # bytes转字符串
        if text.lower() != image_code_server.lower():  # 转小写后比较
            return http.JsonResponse({'code': 4004, 'errmsg': '输入图形验证码有误'})
        # 生成短信验证码：生成6位数验证码
        sms_code = '%06d' % random.randint(0, 999999)
        print("短信验证码是:", sms_code)
        # 保存短信验证码
        redis_conn.setex('sms_%s' % mobile, 3600, sms_code)
        Sms_txy(mobile, sms_code)
        return http.JsonResponse({'errno': 'OK', "errmsg": "发送成功"})
