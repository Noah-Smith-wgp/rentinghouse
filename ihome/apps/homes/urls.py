from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from apps.homes import views


urlpatterns = [
    url(r'^areas/$', views.AreaAPIView.as_view()),
    # url(r'^houses/$', views.HouseAPIView.as_view()),
    url(r'^user/houses/$', views.HouseListView.as_view()),
]

router = DefaultRouter()
# 发布房源
router.register(r'houses', views.HouseAPIView, basename='houses')
urlpatterns += router.urls

# 上传房源图片
router.register(r'houses/(?P<house_id>\d+)/images', views.HouseImageView, basename='images')
urlpatterns += router.urls
