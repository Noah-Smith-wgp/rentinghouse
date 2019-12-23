from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from apps.homes import views


urlpatterns = [
    url(r'^areas/$', views.AreaAPIView.as_view()),
    # url(r'^houses/$', views.HouseAPIView.as_view()),
]

router = DefaultRouter()
router.register(r'houses', views.HouseAPIView, basename='houses')
urlpatterns += router.urls
