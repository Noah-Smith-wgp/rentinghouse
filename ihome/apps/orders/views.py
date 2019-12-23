from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from apps.orders.models import Order
from apps.orders.serializers import OrderInfoSerializer


class OrderInfo(ModelViewSet):
    serializer_class = OrderInfoSerializer
    queryset = Order.objects.all()