from django.conf.urls import url
from apps.verifications import views
urlpatterns = [
    url(r'^imagecode/$', views.UserImagesCode.as_view(), name='image_code'),
    url(r'^sms$', views.SmsCode.as_view(), name='sms_code'),
]