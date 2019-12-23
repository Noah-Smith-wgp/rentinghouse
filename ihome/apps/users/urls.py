from django.conf.urls import url
from .views import userlogin
from .views import userregister

urlpatterns = [
    # 用户登录
    url(r'^session$', userlogin.UserLogin.as_view(), name='login'),
    # 用户注册
    url(r'^users$', userregister.UserRegister.as_view(), name='users')
]
