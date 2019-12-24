from django.conf.urls import url
from .views import userlogin
from .views import userregister
from .views import usercentre

urlpatterns = [
    # 用户登录/退出/判断是否登录
    url(r'^session$', userlogin.UserLoginView.as_view(), name='login'),
    # 用户注册
    url(r'^users$', userregister.UserRegisterView.as_view(), name='users'),
    # 用户中心
    url(r'^user$', usercentre.UserCenterView.as_view(), name='user'),
    # 用户头像
    url(r'^user/avatar$', usercentre.UserImageView.as_view(), name='user_image'),
    # 用户名称
    url(r'^user/name$', usercentre.UserNameView.as_view(), name='user_name'),
    # 实名认证
    url(r'^user/auth$', usercentre.UserAuthView.as_view(), name='user_auth'),
]

# from rest_framework import routers
# router = routers.SimpleRouter()
# router.register(r'user', usercentre.UserCenter, base_name='user')