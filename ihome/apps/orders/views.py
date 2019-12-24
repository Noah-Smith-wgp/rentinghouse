import datetime
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from apps.orders.models import Order
from apps.orders.serializers import OrderInfoSerializer


class OrderInfo(ModelViewSet):

    serializer_class = OrderInfoSerializer
    queryset = Order.objects.all().order_by('-begin_date')

    def get_queryset(self):

        role = self.request.query_params.get('role')
        if role == 'custom':
            return Order.objects.filter(with_landlord=Order.LANDLORD_OR_CUSTOM.get('CUSTOM')).order_by('-begin_date')
        elif role == 'landlord':
            return Order.objects.filter(with_landlord=Order.LANDLORD_OR_CUSTOM.get('LANDLORD')).order_by('-begin_date')

    def list(self, request, *args, **kwargs):
        """订单列表"""

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'data': {'orders': serializer.data},
            'errno': '0',
            'errmsg': 'OK',

        })

    def create(self, request, *args, **kwargs):
        """添加订单"""

        data = request.data
        # data['user'] = request.user
        data['user'] = 1
        data['house_price'] = 289
        data['days'] = (datetime.datetime.strptime(request.data.get('end_date'), '%Y-%m-%d') - datetime.datetime.strptime(request.data.get('begin_date'), '%Y-%m-%d')).days
        data['amount'] = data['house_price'] * data['days']
        data['owner'] = 2
        data['with_landlord'] = Order.LANDLORD_OR_CUSTOM.get('CUSTOM')

        # 保存我的订单(租户视角)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 保存客户订单(房东视角)
        data = serializer.data
        data['with_landlord'] = Order.LANDLORD_OR_CUSTOM.get('LANDLORD')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'data': {'order_id': serializer.data.get('id')},
            'errno': '0',
            'errmsg': '下单成功'
        })

    @action(methods=['put'], detail=True)
    def accept_order(self, request, pk=None):
        """接收订单/拒绝订单"""

        order = self.get_object()
        if request.data.get('action') == 'accept':
            order.status = Order.ORDER_STATUS_ENUM.get('WAIT_ACCEPT')
            order.save()
            return Response({
                "errno": "0",
                "errmsg": "操作成功"
            })
        elif request.data.get('action') == 'reject':
            order.status = Order.ORDER_STATUS_ENUM.get('REJECTED')
            order.comment = request.data.get('reason')
            order.save()
            return Response({
                "errno": "0",
                "errmsg": "操作成功"
            })

    @action(methods=['put'], detail=True)
    def set_comment(self, request, pk=None):
        """评论"""

        order = self.get_object()
        serializer = OrderInfoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "errno": "1",
                "errmsg": "操作失败"
            })
        order.comment = serializer.data.get('comment')
        order.save()
        return Response({
            "errno": "0",
            "errmsg": "评论成功"
        })
