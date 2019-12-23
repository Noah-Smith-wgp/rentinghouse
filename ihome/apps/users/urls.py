from django.conf.urls import url
from .views import userlogin
from .views import userregister
from .views import usercentre

urlpatterns = [
    # 用户登录/退出/判断是否登录
    url(r'^session$', userlogin.UserLogin.as_view(), name='login'),
    # 用户注册
    url(r'^users$', userregister.UserRegister.as_view(), name='users'),
    # 用户中心
    url(r'^user$', usercentre.UserCenter.as_view(), name='user'),
    # 用户头像
    url(r'^user/avatar$', usercentre.UserImage.as_view(), name='user_image'),
    # 用户名称
    url(r'^user/name$', usercentre.UserName.as_view(), name='user_name'),
]

# from rest_framework import routers
# router = routers.SimpleRouter()
# router.register(r'user', usercentre.UserCenter, base_name='user')