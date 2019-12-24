from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from apps.homes import views


urlpatterns = [
    url(r'^areas/$', views.AreaAPIView.as_view()),
    # url(r'^houses/$', views.HouseAPIView.as_view()),
    # 我的房屋列表
    url(r'^user/houses/$', views.HouseListView.as_view()),
    # 首页房屋模块
    url(r'^houses/index/$', views.HouseIndexView.as_view()),
    # 房屋详情页面
    url(r'^houses/(?P<house_id>\d+)/$', views.HouseDetailView.as_view()),
]

router = DefaultRouter()
# # 首页房屋推荐
# router.register(r'houses/index', views.HouseIndexViewSet, basename='index')
# urlpatterns += router.urls
# 发布房源 房屋数据搜索
router.register(r'houses', views.HouseAPIView, basename='houses')
urlpatterns += router.urls

# 上传房源图片
router.register(r'houses/(?P<house_id>\d+)/images', views.HouseImageView, basename='images')
urlpatterns += router.urls

