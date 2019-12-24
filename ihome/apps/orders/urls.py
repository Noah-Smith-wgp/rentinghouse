from django.conf.urls import url, include

from apps.orders import views

urlpatterns = [

    url(r'^user/orders/$', views.OrderInfo.as_view({'get': 'list'})),
    url(r'^orders/$', views.OrderInfo.as_view({'post': 'create'})),
    url(r'^orders/(?P<pk>\d+)/status/$', views.OrderInfo.as_view({'put': 'accept_order'})),
    url(r'^orders/(?P<pk>\d+)/comment/$', views.OrderInfo.as_view({'put': 'set_comment'})),


]
