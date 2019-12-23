from django.conf.urls import url
from .views import userlogin
urlpatterns = [
    url(r'^session$',userlogin.UserLogin.as_view(), name='login')
]
