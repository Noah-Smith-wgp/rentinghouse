from django.conf.urls import url
from apps.verifications import views
urlpatterns = [
    url(r'^imagecode/$', views.UserImagesCode.as_view(), name='image_code'),
]