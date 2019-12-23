from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from apps.homes import views


urlpatterns = [
    url(r'^areas/$', views.AreaAPIView.as_view()),

]

# router = DefaultRouter()
# router.register(r'areas', views.AreaViewSet, basename='areas')
# urlpatterns += router.urls
